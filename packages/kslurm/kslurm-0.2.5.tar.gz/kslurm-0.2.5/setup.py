# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kslurm',
 'kslurm.args',
 'kslurm.installer',
 'kslurm.models',
 'kslurm.slurm',
 'kslurm.style',
 'kslurm.submission']

package_data = \
{'': ['*'], 'kslurm': ['data/*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'colorama>=0.4.4,<0.5.0',
 'rich>=10.9.0,<11.0.0',
 'semver>=2.13.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typing-extensions>=3.10,<4.0']

entry_points = \
{'console_scripts': ['kbatch = kslurm.submission.kbatch:main',
                     'kjupyter = kslurm.submission.kjupyter:main',
                     'krun = kslurm.submission.krun:main',
                     'kslurm = kslurm.kslurm:main']}

setup_kwargs = {
    'name': 'kslurm',
    'version': '0.2.5',
    'description': 'Helper scripts and wrappers for running commands on SLURM compute clusters.',
    'long_description': "Utility functions to make working with SLURM easier.\n\n# Installation\nCluster utils is meant to be run in a SLURM environment, and thus will only install on linux. Open a shell and run the following command:\n\n```\ncurl -sSL https://raw.githubusercontent.com/pvandyken/kslurm/master/install_kslurm.py | python -\n```\n\nIf you wish to uninstall, run the same command with --uninstall added to the end.\n\nThe package can be updated by running `kslurm update`.\n\n# Features\nCurrently offers three commands:\n* kbatch: for batch submission jobs (no immediate output)\n* krun: for interactive submission\n* kjupyter: for Jupyter sessions\n\nAll three use a regex-based argument parsing, meaning that instead of writing a SLURM file or supplying confusing `--arguments`, you can request resources with an intuitive syntax:\n\n```\nkrun 4 3:00 15G gpu\n```\nThis command will request an interactive session with __4__ cores, for __3hr__, using __15GB__ of memory, and a __gpu__.\n\nAnything not specfically requested will fall back to a default. For instance, by default the commands will request 3hr jobs using 1 core with 4GB of memory. You can also run a predefined job template using -j _template_. Run either command with -J to get a list of all templates. Any template values can be overriden simply by providing the appropriate argument.\n\nThe full list of possible requests, their syntaxes, and their defaults can be found at the bottom of the README.\n\n## krun\n\nkrun is used for interactive sessions on the cluster. If you run krun all by itself, it will fire up an interactive session on the cluster:\n\n```\nkrun\n```\nYou'll notice the server name in your terminal prompt will be changed to the cluster assigned to you. To end the session, simply use the `exit` command.\n\nYou can also submit a specific program to run:\n\n```\nkrun 1:00 1G python my_program.py\n```\nThis will request a 1hr session with one core and 1 GB of memory. The output of the job will be displayed on the console. Note that your terminal will be tied to the job, so if you quit, or get disconnected, your job will end. (tmux can be used to help mitigate this, see this [tutorial from Yale](https://docs.ycrc.yale.edu/clusters-at-yale/guides/tmux/) for an excellent overview).\n\nNote that you should never request more than the recommended amount of time for interactive jobs as specified by your cluster administrator. For ComputeCanada servers, you should never request more than 3 hr. If you do, you'll be placed in the general pool for resource assignment, and the job could take hours to start. Jobs of 3hr or less typically start in less than a minute.\n\n## kbatch\n\nJobs that don't require monitoring of the output or immediate submission, or will run for more than three hours, should be submitted using `kbatch`. This command schedules the job, then returns control of the terminal. Output from the job will be placed in a file in your current working directory entitled `slurm-[jobid].out`.\n\nImproving on `sbatch`, `kbatch` does not require a script file. You can directly submit a command:\n\n```\nkbatch 2-00:00 snakemake --profile slurm\n```\nThis will schedule a 2 day job running snakemake.\n\nOf course, complicated jobs can still be submitted using a script. Note that kbatch explictely specifies the resources it knows about in the command line. Command line args override `#SBATCH --directives` in the submit script, so at this time, you cannot use such directives to request resources unless they are not currently supported by kslurm. This may change in a future release.\n\n## kjupyter\n\nThis command requests an interactive job running a jupyter server. As with krun, you should not request a job more than the recommended maximum time for your cluster (3hr for ComputeCanada). If you need more time than that, just request a new job when the old one expires.\n\nYou should not provide any extra command to kjupyter. Just supply whatever resources you wish to request.\n```\nkjupyter 32G 2\n```\nThis will start a jupyter session with 32 GB of memory and 2 cores.\n\nNote that the command will fail if there is no `jupyter-lab` executable on the `PATH`. Use `pip install jupyterlab` if it's not installed. Typically, you should do this within a Python environment using a tool of your choice (e.g. virtualenv).\n\n# Unsupported SLURM args\n\nCurrently, the only way to supply arguments to SLURM beyond the items listed below is to list it as an `#SBATCH --directive` in a submission script. This only works with `kbatch`, not `krun` or `kjupyter`. A future release may support a method to supply these arguments directly on the command line. If you frequently use an option not listed below, make an issue and we can discuss adding support!\n\n# Slurm Syntax\n\nThe full syntax is outlined below. You can always run a command with `-h` to get help.\n\n| Resource  |           Syntax           |                                                                   Default |                                                    Description |\n| :-------- | :------------------------: | ------------------------------------------------------------------------: | -------------------------------------------------------------: |\n| Time      | [d-]dd:dd -> [days-]hh:mm  |                                                                       3hr |                                   The amount of time requested |\n| CPUS      |     d -> just a number     |                                                                         1 |                                   The number of CPUs requested |\n| Memory    |            d(G/M)[B] -> e.g. 4G, 500MB |                                                            4GB | The amount of memory requested |\n| Account   | --account <_account name_> | Currently hard coded to ctb-akhanf. Eventually will support configuration |                      The account under which to submit the job |\n| GPU       |            gpu             |                                                                     False |                         Provide flag to request 1 GPU instance |\n| Directory |  <_any valid directory_>   |                                                                        ./ | Change the current working directory before submitting the job |\n| x11       |           --x11            |                                                                     False |                   Requests x11 forwarding for GUI applications |\n",
    'author': 'Peter Van Dyken',
    'author_email': 'pvandyk2@uwo.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pvandyken/kslurm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
