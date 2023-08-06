import pdme.model
from typing import Sequence, Tuple, List
import datetime
import itertools
import csv
import logging
import numpy
import scipy.optimize
import multiprocessing


# TODO: remove hardcode
COST_THRESHOLD = 1e-10


# TODO: It's garbage to have this here duplicated from pdme.
DotInput = Tuple[numpy.typing.ArrayLike, float]


_logger = logging.getLogger(__name__)


def get_a_result(
	discretisation, dots, index
) -> Tuple[Tuple[int, ...], scipy.optimize.OptimizeResult]:
	return (index, discretisation.solve_for_index(dots, index))


class BayesRun:
	"""
	A single Bayes run for a given set of dots.

	Parameters
	----------
	dot_inputs : Sequence[DotInput]
	The dot inputs for this bayes run.

	discretisations_with_names : Sequence[Tuple(str, pdme.model.Model)]
	The models to evaluate.

	actual_model_discretisation : pdme.model.Discretisation
	The discretisation for the model which is actually correct.

	filename_slug : str
	The filename slug to include.

	run_count: int
	The number of runs to do.
	"""

	def __init__(
		self,
		dot_inputs: Sequence[DotInput],
		discretisations_with_names: Sequence[Tuple[str, pdme.model.Discretisation]],
		actual_model: pdme.model.Model,
		filename_slug: str,
		run_count: int,
		max_frequency: float = None,
		end_threshold: float = None,
	) -> None:
		self.dot_inputs = dot_inputs
		self.discretisations = [disc for (_, disc) in discretisations_with_names]
		self.model_names = [name for (name, _) in discretisations_with_names]
		self.actual_model = actual_model
		self.model_count = len(self.discretisations)
		self.run_count = run_count
		self.csv_fields = ["dipole_moment", "dipole_location", "dipole_frequency"]
		self.compensate_zeros = True
		for name in self.model_names:
			self.csv_fields.extend([f"{name}_success", f"{name}_count", f"{name}_prob"])

		self.probabilities = [1 / self.model_count] * self.model_count

		timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
		self.filename = f"{timestamp}-{filename_slug}.csv"
		self.max_frequency = max_frequency

		if end_threshold is not None:
			if 0 < end_threshold < 1:
				self.end_threshold: float = end_threshold
				self.use_end_threshold = True
				_logger.info(f"Will abort early, at {self.end_threshold}.")
			else:
				raise ValueError(
					f"end_threshold should be between 0 and 1, but is actually {end_threshold}"
				)

	def go(self) -> None:
		with open(self.filename, "a", newline="") as outfile:
			writer = csv.DictWriter(outfile, fieldnames=self.csv_fields, dialect="unix")
			writer.writeheader()

		for run in range(1, self.run_count + 1):
			frequency: float = run
			if self.max_frequency is not None and self.max_frequency > 1:
				rng = numpy.random.default_rng()
				frequency = rng.uniform(1, self.max_frequency)
			dipoles = self.actual_model.get_dipoles(frequency)

			dots = dipoles.get_dot_measurements(self.dot_inputs)
			_logger.info(f"Going to work on dipole at {dipoles.dipoles}")

			results = []
			_logger.debug("Going to iterate over discretisations now")
			for disc_count, discretisation in enumerate(self.discretisations):
				_logger.debug(f"Doing discretisation #{disc_count}")
				with multiprocessing.Pool(multiprocessing.cpu_count() - 1 or 1) as pool:
					results.append(
						pool.starmap(
							get_a_result,
							zip(
								itertools.repeat(discretisation),
								itertools.repeat(dots),
								discretisation.all_indices(),
							),
						)
					)

			_logger.debug("Done, constructing output now")
			row = {
				"dipole_moment": dipoles.dipoles[0].p,
				"dipole_location": dipoles.dipoles[0].s,
				"dipole_frequency": dipoles.dipoles[0].w,
			}
			successes: List[float] = []
			counts: List[int] = []
			for model_index, (name, result) in enumerate(
				zip(self.model_names, results)
			):
				count = 0
				success = 0
				for idx, val in result:
					count += 1
					if val.success and val.cost <= COST_THRESHOLD:
						success += 1

				row[f"{name}_success"] = success
				row[f"{name}_count"] = count
				successes.append(max(success, 0.5))
				counts.append(count)

			success_weight = sum(
				[
					(succ / count) * prob
					for succ, count, prob in zip(successes, counts, self.probabilities)
				]
			)
			new_probabilities = [
				(succ / count) * old_prob / success_weight
				for succ, count, old_prob in zip(successes, counts, self.probabilities)
			]
			self.probabilities = new_probabilities
			for name, probability in zip(self.model_names, self.probabilities):
				row[f"{name}_prob"] = probability
			_logger.info(row)

			with open(self.filename, "a", newline="") as outfile:
				writer = csv.DictWriter(
					outfile, fieldnames=self.csv_fields, dialect="unix"
				)
				writer.writerow(row)

			if self.use_end_threshold:
				max_prob = max(self.probabilities)
				if max_prob > self.end_threshold:
					_logger.info(
						f"Aborting early, because {max_prob} is greater than {self.end_threshold}"
					)
					break
