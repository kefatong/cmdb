__author__ = 'eric'



from app import create_app,db
#from app.models import User, Role,Idc, Rack, Asset, Device, DeviceType, DeviceDisks, Logger, DevicePorts, DeviceMemorys, VirtMachine, DevicePowerManage, DevicePools
from app.models import *
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Idc=Idc, Rack=Rack,
                Asset=Asset, Device=Device, DeviceDisks=DeviceDisks,
                Logger=Logger, DevicePorts=DevicePorts, DeviceMemorys=DeviceMemorys,
                DevicePools=DevicePools, DevicePower=DevicePower, VirtMachine=VirtMachine,
                DevicePortMap=DevicePortMap, DeviceNetwork=DeviceNetwork, ClassType=ClassType,
                DeviceModel=DeviceModel, IpResourcePools=IpResourcePools, IpResourceManage=IpResourceManage,
                ServiceProvider=ServiceProvider, ServiceProviderContact=ServiceProviderContact)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
