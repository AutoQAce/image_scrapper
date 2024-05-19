import os

from app import create_app
from app.config import Config,TestConfig

import argparse

"""
    to run the command....
 
    python run.py (Uses default ProductionConfig)
    python run.py -c testing (Uses TestingConfig)
    python run.py --config production (Uses ProductionConfig)

"""

def main():
    # this is more userfriendly and explicit so can be used while running for the local system
    parser = argparse.ArgumentParser(description='Run the application with a specific configuration.')
    parser.add_argument('-c', '--config', choices=['testing', 'production'], default='production',
                        help='Configuration to use (default: production)')
    args=parser.parse_args()

    #config_name=os.environ.get('FLASK_CONFIG','production') # Useful for automation and deployment of the code
    """
        On Linux/macOS: export FLASK_CONFIG=testing
        On Windows: set FLASK_CONFIG=testing 
    """
    config_class={
        "testing": TestConfig,
        "production":Config
    }.get(args.config,Config) # will get the argument from the config class dictornary.. if no match found then it will give Config as default.
    app=create_app(config_class)
    app.run()

if __name__=='__main__':
    main()

