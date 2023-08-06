=============================
sandtank-xai
=============================

AI/XAI exploration in the context of ParFlow simulation code


* Free software: BSD License


Installing
-----------------------------
Build and install the Vue components

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -

For the Python layer it is recommended to use conda to properly install the various ML packages.

macOS conda setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    brew install miniforge
    conda init zsh

venv creation for XAI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    conda create --name sandtank-xai python=3.9 -y
    conda activate sandtank-xai
    conda install "pytorch==1.11.0" -c pytorch -y
    conda install scipy "scikit-learn==0.24.2" "scikit-image==0.18.3" -c conda-forge -y

    # A: For development when inside repo (A or B not both)
    pip install -e .

    # B: For testing without repo (A or B not both)
    pip install trame-sandtank-xai


Run the application

.. code-block:: console

    conda activate sandtank-xai
    trame-sandtank-xai
