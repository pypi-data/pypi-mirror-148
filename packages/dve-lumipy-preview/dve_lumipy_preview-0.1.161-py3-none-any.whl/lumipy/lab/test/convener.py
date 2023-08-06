import datetime as dt
import os
import time
import uuid
from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import clear_output

from lumipy.common.string_utils import indent_str
from .base import BaseExperiment


class Convener:
    """The convener class looks after the running of experiments and recording their data.

    """

    def __init__(
            self,
            experiment: BaseExperiment,
            work_dir: str,
            name: str,
            n_obs: int,
            **kwargs
    ):
        """Constructor of the convener class.

        Args:
            experiment (BaseExperiment): the experiment to run.
            work_dir (str): the working directory to write results to.
            name (str): the name of the experiment.
            n_obs (int): number of times to run the experiment and observe values.

        Keyword Args:
             seed (Optional[int]): random seed to set at the start of the experimental run. Will be chosen randomly if
             not specified.
             err_wait (Optional[int]): number of seconds to wait after getting an error.
             n_parallel (Optional[Union[int, List[int]]]): number of concurrent runs of the experiment to run each time.

        """

        self.__work_dir = work_dir
        self.__name = name
        self.__experiment = experiment
        self.__n_obs = n_obs
        self.__seed = kwargs.get('seed', np.random.randint(1989))
        self.__err_wait = kwargs.get('err_wait', 15)
        self.__n_parallel = kwargs.get('n_parallel', 1)
        self.__force_stop = False

        data_dir = f'{self.__work_dir}/data'
        self.__data_file = f'{data_dir}/{self.__name}.csv'

        Path(data_dir).mkdir(parents=True, exist_ok=True)
        Path(f'{self.__work_dir}/plots').mkdir(parents=True, exist_ok=True)

    def __job(self) -> pd.DataFrame:

        if isinstance(self.__n_parallel, int):
            n_parallel = self.__n_parallel
        else:
            np.random.seed((dt.datetime.utcnow() - dt.datetime(1970, 1, 2)).seconds)
            n_parallel = np.random.randint(self.__n_parallel[0], self.__n_parallel[1] + 1)

        if n_parallel > 1:
            print(f'    Running {n_parallel} concurrent queries')
            print(f'    Only showing a log for the first one.', end='\n\n')

        tasks = [self.__experiment.copy(self.__seed, i != 0) for i in range(n_parallel)]
        try:
            for t in tasks:
                t.start()
            df = pd.DataFrame([t.join(force=False) for t in tasks])

        except KeyboardInterrupt:
            print("\n🛑 Quitting the experimental run...\n")
            df = pd.DataFrame([t.join(force=True) for t in tasks])
            self.__force_stop = True

        df['n_parallel'] = n_parallel
        return df

    def go(self) -> None:
        """Run the experiments.

        Notes:
            Can be halted with keyboard interrupt.

        """

        error_count = 0
        run_start = dt.datetime.utcnow()
        offset = dt.datetime.now() - dt.datetime.utcnow()

        # Very important. Do not remove.
        emoji = np.random.choice(['🧪', '🔭', '⚗️', '🧬', '🔬', '📐'])

        times = []
        start = None
        for i in range(1, self.__n_obs + 1):
            clear_output(wait=True)
            print(f"Doing Science! {emoji}")
            print(f"  Experiment name: {self.__name}")
            print(f"  Run started at: {(run_start + offset).strftime('%Y-%m-%d %H:%M:%S')}")

            new_start = dt.datetime.utcnow()
            if start is not None:
                times.append((new_start - start).total_seconds())
            start = new_start

            if len(times) > 1:
                t_mean = np.mean(times)
                t_std_err = np.std(times) / np.sqrt(len(times) - 1)
                est_len = self.__n_obs * t_mean / 60
                est_len_stderr = (self.__n_obs * (t_std_err**2))**0.5
                est_finish = run_start + dt.timedelta(minutes=est_len) + offset
                print(f"    Mean experiment time: {t_mean:2.2f}s ±{t_std_err:2.2}s")
                print(f"    Estimated total experiment time: {est_len:2.2f}min ±{est_len_stderr:2.2f}s → finish @ {est_finish.strftime('%H:%M:%S')}")

            if len(times) > 0:
                print(f"    Error count: {error_count}")

            print(f"\n    Experiment {i}/{self.__n_obs} started at {(start + offset).strftime('%H:%M:%S')}")

            df = self.__job()
            df['experiment_name'] = self.__name
            df['run_start'] = run_start
            df['experiment_id'] = str(uuid.uuid4())
            df.to_csv(self.__data_file, index=False, mode='a', header=not os.path.exists(self.__data_file))

            if self.__force_stop:
                break

            if any(df['errored'].tolist()):
                error_count += 1
                print(f"Waiting {self.__err_wait}s after getting an error...")
                err_msg = indent_str('\n'.join(e for e in df['error_message'] if e is not None), 4)
                print(f"Error:\n{err_msg}")
                time.sleep(self.__err_wait)

            self.__seed += 1

            print(f'\nAppending data to {self.__data_file}')
            finish = dt.datetime.utcnow() + offset
            print(f"Finished data taking at {finish.strftime('%H:%M:%S')}")

    @property
    def data_file_path(self) -> str:
        """Get the file path for the results data CSV.

        Returns:
            str: the data csv file path
        """
        return self.__data_file

    def read_csv(self) -> pd.DataFrame:
        """Read the results data CSV and return it as a pandas dataframe.

        Returns:
            DataFrame: the contents of the data CSV file.
        """
        return pd.read_csv(self.__data_file)
