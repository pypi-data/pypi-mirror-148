**[Installation](#installation)** |
**[Execution](#execution)** |
**[Authorization](#authorization)** |
**[Further documentation](#further-documentation)** |
**[Getting help](#getting-help)** |

# JuMonC

JuMonC stands for "Jülich monitoring and control" and allows easier access to monitor running simulations and provides data using a REST-API.

---

## Installation

JuMonC can be installed using [pip](https://pypi.org/project/JuMonC/):

`pip install JuMonC`

This also creates an entry point, allowing to start JuMonC with just the command `JuMonC`

### Runtime dependencies

- python3
- [mpi4py](https://mpi4py.readthedocs.io/en/stable/)
- [flask](https://flask.palletsprojects.com/en/2.0.x/)
- [flask-login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](https://github.com/pallets-eco/flask-sqlalchemy)

### Optional runtime dependencies

- [python-papi](https://flozz.github.io/pypapi/install.html)
- [pynvml](https://pypi.org/project/pynvml/)
- [psutil](https://pypi.org/project/psutil/)



## Execution

JuMonC needs to be started parallel to your running simulation and needs one mpi process on each node your simulation is using. The actual REST-API will only be avaiable on node 0 and then communicate internaly using mpi.

It can be started by running `srun -n <#nodes> --ntasks-per-node=1 JuMonC &`

By default, this will start the REST-API on port 12121 on rank 0 of this allocation. The port can be changed by providing `-p=<port>`. Depending on the firewall rules of the system you are using, it might be necessary to use a ssh-tunnel to forward this endpoint of the API to somewhere else where you can access it.


## Authorization

Security is always a concern, and to block unauthorized access of this API there is a scope based token authorization included. This means each action requires authorization, with different tokens having a different scope of allowed actions. The tokens included by default and printed to `stdout` on startup are hierarchical, therefore every token includes the authorized functions of all lower tokens:

1. see_links
2. retrieve_data
3. compute_data
4. retrieve_simulation_data
5. compute_simulation_data
6. full

There are two options to prove your authorization, either cookie based by providing the token once in the login function (e.g. `/login?token=12345678`) or providing it by every API call as an additional parameter (e.g. `/v1/network?token=12345678`).

## Further documentation

- [REST-API](doc/REST_API/openapi.yaml)
- [Possible cmd arguments](doc/CMD/Parameters.md) or using the `-h` flag
- [JuMonC_overview](doc/Developer/JuMonC_overview.ipynb)


## Getting help



