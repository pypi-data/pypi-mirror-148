[![Documentation Status](https://readthedocs.org/projects/invertedai-simulate/badge/?version=latest)](https://invertedai-simulate.readthedocs.io/en/latest/?badge=latest)

#   Product Interface Client

<!-- start elevator-pitch -->
- **Safety Validation**
- **Synthetic Data Generation** 
- **Training and Testing**
- **Real-World Results From Simulation** 
<!-- end elevator-pitch -->



<!-- start quickstart -->
1. Install invertedai_simulate in your project environment.

   ```shell
   pip install invertedai_simulate
   ```

2. Alternatively, to run the provided examples build the environment with the packages in the 'requirements.txt'.
   ```shell
   pip install -r requirements.txt
   source .venv/bin/activate
   ```
4. Contact us for the server ip address.
3. Run your simulation! 🎉
- For driving run:
  ```shell
   python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'
  ```
- For data generation run:
   ```shell
   python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'
   ```

<!-- end quickstart -->

### Building
`python -m build`
