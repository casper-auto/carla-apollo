# cyber / bridge requirements
# sudo apt update && \
#     apt install -y python-pip && \

pip install --upgrade pip
pip install \
    numpy \
    opencv-python==4.2.0.32 \
    protobuf \
    pygame \
    pyproj \
    pyyaml \
    transforms3d

echo "source /apollo/cyber/setup.bash" >> ~/.bashrc
echo "export CARLA_PYTHON_ROOT=/apollo/cyber/carla_bridge/carla_python" >> ~/.bashrc
echo "export PYTHONPATH=\$PYTHONPATH:/apollo/py_proto" >> ~/.bashrc
echo "export PYTHONPATH=\$PYTHONPATH:\$CARLA_PYTHON_ROOT/carla/dist/carla-0.9.11-py2.7-linux-x86_64.egg" >> ~/.bashrc
echo "export PYTHONPATH=\$PYTHONPATH:\$CARLA_PYTHON_ROOT/carla" >> ~/.bashrc
echo "" >> ~/.bashrc
