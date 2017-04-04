import auxiliary
import dbmodel
import sqlalchemy
import os
import sys
import paramiko
import hashlib
from prettytable import PrettyTable
from sqlalchemy import inspect

def timezone():
    os.system('timedatectl | grep \"Timezone\"')
