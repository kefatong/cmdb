#coding:utf8

_author__ = 'eric'


from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Email, Length, Regexp, EqualTo, InputRequired, IPAddress, HostnameValidation, MacAddress, NumberRange
from ..models import Role, Rack, Asset, Device, DeviceType, Idc, DeviceDisks, DevicePorts, DeviceMemorys, DevicePools, DevicePowerManage
from wtforms import ValidationError


class NameForm(Form):
    name = StringField('what is your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    username = StringField('Username', validators=[InputRequired(), Length(0,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    name = StringField(u'真实姓名', validators=[InputRequired(), Length(0,64)])
    position = StringField(u'工作职位', validators=[InputRequired(), Length(0,64)])
    qq = StringField(u'QQ号码')
    phone = StringField(u'手机号码')
    location = StringField(u'位置', validators=[Length(0,64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField('Email',validators=[InputRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[InputRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    confirmed = BooleanField(u'confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')


class EditDeviceTypeForm(Form):
    name = StringField(u'资产类名', validators=[InputRequired() ,Length(1,64)])             # 资产类名
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, deviceType, *args, **kwargs):
        super(EditDeviceTypeForm, self).__init__(*args, **kwargs)
        self.deviceType = deviceType

    def validate_name(self,field):
        if not self.deviceType:
            if DeviceType.query.filter_by(name=field.data).first():
                raise ValidationError(u'资产类名已经被使用了')
        else:
            if field.data != self.deviceType.name and DeviceType.query.filter_by(name=field.data).first():
                raise ValidationError(u'资产类名已经被使用了')


class EditIdcForm(Form):
    name = StringField(u'Idc名称', validators=[InputRequired() ,Length(1,64)])
    ispid = StringField(u'运营商名称', validators=[InputRequired() ,Length(1,64)])                        # 运营商名称
    city = StringField(u'城市', validators=[InputRequired() ,Length(1,64)])                         # 城市
    address = StringField(u'机房地址', validators=[InputRequired() ,Length(1,64)])                     # 机房地址
    contactname = StringField(u'联系人姓名', validators=[InputRequired() ,Length(1,64)])
    contactphone = StringField(u'联系人电话', validators=[InputRequired() ,Length(1,64)])
    nettype = SelectField(u'网络类型', coerce=int)                      # 网络类型
    netout = StringField(u'出口带宽', validators=[InputRequired() ,Length(1,64)])                       # 出口带宽
    adnature = SelectField(u'机房类型', coerce=int)                     # 机房性质
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, idc, *args, **kwargs):
        super(EditIdcForm, self).__init__(*args, **kwargs)

        self.nettype.choices = [(1, u'单电信'), (2, u'单联通'), (3, u'双BGP'), (4, u'联通电信双线')]

        self.adnature.choices = [(1, u'租用'), (2, u'自建'), (3, u'合作'), (4, u'其他')]

        self.idc = idc

    def validate_name(self,field):
        if not self.idc:
            if Idc.query.filter_by(name=field.data).first():
                raise ValidationError(u'机房名称已经被使用了')
        else:
            if field.data != self.idc.name and Idc.query.filter_by(name=field.data).first():
                raise ValidationError(u'机房名称已经被使用了')


class EditAssetForm(Form):
    DeviceType = SelectField(u'设备类型', coerce=int)   # 资产类别   关联AssetType table
    an = StringField(u'AN号', validators=[InputRequired() ,Length(1,64)])   # AN 企业资产编号
    sn = StringField(u'SN号', validators=[InputRequired() ,Length(1,64)])                           # SN 设备序列号
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    dateofmanufacture = DateTimeField(u'生产时间')              # 生产时间
    manufacturer = StringField(u'生产商', validators=[Length(1,64)])                 # 生产商
    brand = StringField(u'品牌', validators=[Length(1,64)])                        # 品牌
    model = StringField(u'型号', validators=[Length(1,64)])                        # 型号
    usedept = StringField(u'使用部门', validators=[Length(1,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(1,64)])                     # 部门使用人
    usestarttime = DateTimeField(u'使用开始时间')                   # 使用开始时间
    useendtime = DateTimeField(u'使用结束时间')                     # 使用结束时间
    mainuses = StringField(u'主要用途', validators=[Length(1,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(1,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(1,64)])                  # 管理人
    koriyasustarttime = DateTimeField(u'维保开始时间')              # 维保开始时间
    koriyasuendtime = DateTimeField(u'维保结束时间')                # 维保结束时间
    equipprice = IntegerField(u'设备价格')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditAssetForm, self).__init__(*args, **kwargs)

        self.DeviceType.choices = [(deviceType.id, deviceType.name)
                             for deviceType in DeviceType.query.order_by(DeviceType.name).all()]

        self.onstatus.choices = [(1, u'使用'), (2, u'下线')]


    def validate_an(self,field):
        if Device.query.filter_by(an=field.data).first():
            raise ValidationError(u'AN已经被使用了')

    def validate_sn(self,field):
        if Device.query.filter_by(sn=field.data).first():
            raise ValidationError(u'SN已经被使用了')


class EditDeviceForm(Form):
    DeviceType = SelectField(u'设备类型', coerce=int)   # 资产类别   关联AssetType table
    an = StringField(u'AN号', validators=[InputRequired() ,Length(1,64)])   # AN 企业资产编号
    sn = StringField(u'SN号', validators=[InputRequired() ,Length(1,64)])                           # SN 设备序列号
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    dateofmanufacture = DateTimeField(u'生产时间')              # 生产时间
    manufacturer = StringField(u'生产商', validators=[Length(1,64)])                 # 生产商
    brand = StringField(u'品牌', validators=[Length(1,64)])                        # 品牌
    model = StringField(u'型号', validators=[Length(1,64)])                        # 型号
    usedept = StringField(u'使用部门', validators=[Length(1,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(1,64)])                     # 部门使用人
    mainuses = StringField(u'主要用途', validators=[Length(1,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(1,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(1,64)])                  # 管理人

    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    rack = SelectField(u'机柜', coerce=int)                  # 关联Rack table id
    devicePorts = StringField(u'设备接口')
    is_virtualization = BooleanField(u'虚拟化')               # 是否跑虚拟化  （如 OpenStack Compute）
    os = StringField(u'操作系统')
    cpumodel = StringField(u'CPU型号', validators=[Length(0,64)])                     # CPU 型号
    cpucount = IntegerField(u'CPU内核(个)')                        # CPU 核数
    memsize = IntegerField(u'内存大小(GB)')                      # 内存容量
    memorys = StringField(u'设备内存')
    raidmodel = StringField(u'Raid级别', validators=[Length(0,16)])                    # RAID 级别
    disksize = IntegerField(u'磁盘大小(GB)')                        # 磁盘容量
    disks = StringField(u'设备磁盘')
    use = StringField(u'用途')
    businss = SelectField(u'所属业务', coerce=int)
    powerstatus = BooleanField(u'电源状态')
    powermanage = SelectField(u'电源管理', coerce=int)


    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceForm, self).__init__(*args, **kwargs)

        self.onstatus.choices = [(1, u'未用'), (2, u'已用')]

        self.rack.choices = [(rack.id, rack.name)
                             for rack in Rack.query.order_by(Rack.name).all()]

        self.businss.choices = [(1, u'云计算',),]

        self.powerstatus.choices = [(1, u'开机'), (2, u'关机')]



class EditVritMachineForm(Form):
    deviceType = SelectField(u'设备类型', coerce=int)   # 资产类别   关联AssetType table
    onstatus = SelectField(u'使用状态', coerce=int)                        # 使用状态
    usedept = StringField(u'使用部门', validators=[Length(1,64)])                       # 使用部门
    usestaff = StringField(u'部门使用人', validators=[Length(1,64)])                     # 部门使用人
    mainuses = StringField(u'主要用途', validators=[Length(1,128)])                    # 主要用途
    managedept = StringField(u'管理部门', validators=[Length(1,64)])                   # 管理部门
    managestaff = StringField(u'管理人', validators=[Length(1,64)])                  # 管理人
    device = SelectField(u'运行主机', coerce=int)
    pool = SelectField(u'资源池', coerce=int)
    hostname = StringField(u'主机名', validators=[HostnameValidation, Length(0,64)])
    os = StringField(u'操作系统')
    cpumodel = StringField(u'CPU型号', validators=[Length(0,64)])                     # CPU 型号
    cpucount = IntegerField(u'CPU内核(个)')                        # CPU 核数
    memsize = IntegerField(u'内存大小(GB)')                      # 内存容量
    disksize = IntegerField(u'磁盘大小(GB)')                        # 磁盘容量
    businss = SelectField(u'所属业务', coerce=int)
    powerstatus = BooleanField(u'电源状态')
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditVritMachineForm, self).__init__(*args, **kwargs)

        self.deviceType.choices = [(1, u'虚拟机'),]

        self.onstatus.choices = [(1, u'未用'), (2, u'已用')]

        self.device.choices = [(device.id, device.hostname)
                             for device in Device.query.order_by(Device.hostname).all()]

        self.pool.choices = [(pool.id, pool.name)
                             for pool in DevicePools.query.order_by(DevicePools.name).all()]

        self.businss.choices = [(1, u'云计算',),]

        self.powerstatus.choices = [(1, u'开机'), (2, u'关机')]


class EditDevicePortForm(Form):
    name = StringField(u'接口名称', validators=[InputRequired(), Length(1,64)])
    ip = StringField(u'IP地址')
    mac = StringField(u'Mac地址')
    portType = StringField(u'接口类型')
    device = SelectField(u'设备', coerce=int)
    to_device = SelectField(u'连接至')
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDevicePortForm, self).__init__(*args, **kwargs)

        self.device.choices = [(device.id, device.hostname)
                             for device in Device.query.order_by(Device.hostname).all()]

        self.to_device.choices = [(ports.id, '{0}.{1}'.format(ports.device.device.hostname, ports.name))
                             for ports in DevicePorts.query.order_by(DevicePorts.name).all()
                                  if not ports.to_device_src and not ports.to_device_dest]


class EditDeviceMemoryForm(Form):
    slot_id = StringField(u'内存插槽', validators=[InputRequired(), Length(1,64)])
    SN = StringField(u'序列号')
    Size = IntegerField(u'内存大小')
    device = SelectField(u'设备', coerce=int)
    remarks = TextAreaField(u'备注')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDeviceMemoryForm, self).__init__(*args, **kwargs)

        self.device.choices = [(device.id, device.hostname)
                             for device in Device.query.order_by(Device.hostname).all()]


class EditDevicePowermanageForm(Form):
    powermanageType = SelectField(u'电源模块', coerce=int)                      # 网络类型
    powermanageEnable = BooleanField(u'启用电源管理')
    powermanageIp = StringField(u'电源管理IP', validators=[Length(0,15)])                 # 远控卡IP地址
    powermanageUser = StringField(u'电源管理用户', validators=[Length(0,64)])
    powermanagePassword = StringField(u'电源管理密码', validators=[Length(0,64)])
    powermanageId = StringField(u'设备ID', validators=[Length(0,64)])          # 缃戝崱绔彛鏁伴噺
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(EditDevicePowermanageForm, self).__init__(*args, **kwargs)

        self.powermanageType.choices = [(1, u'直流'), (1, u'交流')]

#    def validate_powermanage_ip(self, field):
#        if DevicePowerManage.query.filter_by(powermanage_ip=field.data).first():
#            raise ValidationError(u'远控卡IP: {0}已经用了'.format(field.data))



class EditDevicePoolsForm(Form):
    name = StringField(u'资源池名称', validators=[InputRequired(), Length(1,64)])
    remarks = TextAreaField(u'备注')                          # 备注
    submit = SubmitField(u'提交')



class EditRackForm(Form):
    name = StringField(u'机柜名称', validators=[InputRequired(), Length(1,64)])
    staff = StringField(u'管理人', validators=[Length(0,64)])                        # 机柜负责人
    idcname = SelectField(u'机房', coerce=int)
    site = StringField(u'机柜位置', validators=[Length(1,64)])                         # 机柜位置
    racktype = SelectField(u'机柜类型', coerce=int)                     # 机柜类型
    usesize = IntegerField(u'已用(u)')                      # 已用空间（u）
    remainsize = IntegerField(u'可用(u)')                   # 剩余空间（U）
    electrictype = SelectField(u'电力类型', coerce=int)                 # 电力类型
    electricno = SelectField(u'电力路数', coerce=int)                   # 电力路数
    electriccapacity = IntegerField(u'电力容量(A)')             # 电力容量
    leftelectric = IntegerField(u'剩余容量(A)')                 # 剩余电力
    renttime = DateTimeField(u'租用时间')                   # 租用时间
    expiretime = DateTimeField(u'过期时间')                     # 过期时间
    nextpaytime = DateTimeField(u'下次支付时间')                    # 下次支付时间
    money = IntegerField(u'支付金额')                        # 支付金额
    remarks = TextAreaField(u'备注')                            # 备注
    submit = SubmitField(u'提交')

    def __init__(self, rack,*args, **kwargs):
        super(EditRackForm, self).__init__(*args, **kwargs)

        self.idcname.choices = [(idc.id, idc.name)
                             for idc in Idc.query.order_by(Idc.name).all()]

        self.racktype.choices = [(1, u'网络设备'), (2, u'服务器')]

        self.electrictype.choices = [(1, u'直流'), (1, u'交流')]

        self.electricno.choices = [(1, u'单路'), (1, u'双路')]

        self.rack = rack

    def validate_name(self, field):
        if not self.rack:
            if Rack.query.filter_by(name=field.data).first():
                raise ValidationError(u'机柜名已经创建了')
        else:
            if field.data != self.rack.name and Rack.query.filter_by(name=field.data).first():
                raise ValidationError(u'机柜名已经创建了')
