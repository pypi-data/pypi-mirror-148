方法目录
=
---

b_c_components：
=

 获取当前时间段内页面所产生的请求方法: info

         引用路径:from b_c_components.Intercept_requests.selenium_network import info
         入参:driver实体对象
         返回:一个嵌套字典的List集合
        info方法已经升级为get_network_data,后续再次使用请使用get_network_data
 获取当前时间段内页面所产生的请求方法: get_network_data（info升级版）

     引用路径:from b_c_components.Intercept_requests.selenium_network import get_network_data
     入参:driver实体对象
     返回:一个嵌套字典的List集合
     info方法已经升级为get_network_data,后续再次使用请使用get_network_data
     方法说明： 获取当前driver记录的所有日志（日志每次获取后，获取的日志不会留存）

获取当前用例执行期间的所有请求： get_case_all_network_data

     引用路径:from b_c_components.Intercept_requests.selenium_network import get_case_all_network_data
     入参:driver实体对象
     返回:一个嵌套字典的List集合


 获取指定接口返回的response的body： get_interface_body

      引用路径:from b_c_components.Intercept_requests.selenium_network import get_interface_body
      入参:driver实体对象， interface_name：接口地址（协议+域名+/接口地址?参数）
      返回:body
 获取excel内容类: 

         引用路径 from b_c_components.get_excel.do_excel import do_excel 
         类初始化参数: 
                 r_filename:Excel文件路径， 必填 
                 r_sheet_name: sheet名称，非必填，无值时，取第一个sheet 
         类方法:read_excel 
                 is_namedtuple: 是否返回命名元组，1是，0返回excel所有列的list嵌套 
                 min_row: 读取数据从最小的第几行开始读取 
                 max_col: 读取数据最大列到第几列 
                 namedtuple_name: 命名元组名称 
                 col: 命名元组获取的名称为多行时，指定第几行为元组的key 
                 namedtuple_min_row:命名元组获取名称从第几行开始获取 
                 namedtuple_max_row:命名元组获取名称到第几行终止 
                 namedtuple_min_col:命名元组获取名称从第几列开始获取 
                 namedtuple_max_col:命名元组获取名称到第几列终止 
         返回list集合（集合内嵌套字典｜命名元组） 
 读取config配置文件: 

         引用路径: from b_c_components.get_config import Settings 
         类初始化参数: 
                 config_path:配置文件的绝对路径 
         类方法: get_setting 
                 section: 区块名称 
                 my_setting: setting名称 
         返回:string类型的数据 
         类方法: get_int 
                 section: 区块名称 
                 my_setting: setting名称 
         返回:int类型的数据 
 自动根据当前系统的chrome版本获取chromedriver对应版本的驱动 

         引用路径: from b_c_components.get_b_version.get_version import auto_get_browser_driver 
         入参: 
                 config_path 方法依赖配置文件的路径 
         返回参数: 下载好的驱动地址 
         配置文件中的节点: 
                 [windows_browser_path] 
                 chrome_browser_path = 当前windows操作系统的chrome执行文件地址 
                 service_chrome_browser_path = C:\Program Files\Google\Chrome\Application\chrome.exe # 40.28服务器的chrome执行文件地址
                 [mac_browser_plist_path]
                 chrome_list_path = 当前mac操作系统的chrome执行文件地址
 自定义异常类型类:

         引用路径: from b_c_components.custom_module.custom_exceptions import Configuration_file_error
         类初始化参数:Configuration_file_error(msg='自定义返回错误信息')
         抛出异常类型为:Configuration_file_error
         抛出异常内容为:定义的msg，不定义默认为空
 log封装类:

         引用路径:from b_c_components.log.log import Logging
         类初始化参数:
                 log_path:log落地文件地址
                 loh_Level: log等级，默认值为INFO
         例:

            def demo():
                 log = Logging("path/log.log", 'DEBUG')
                 try:
                     int("触发异常")
                 except Exception as e:
                     log.logger.log(log.logger.level, msg=e)
 获取环境对应url：

    引用路径:from b_c_components.get_environment_data import get_environment_data
    方法参数：environment， 默认值None
        参数为none时，优先调用临时环境变量中的environment值；
        environment值为空时，调用配置文件获取environment；以上兼容，需要前置定义环境变量

---
v3_components:
=
UI登陆接口类 v3_login_ui:

    引用路径: from v3_components.page.login import v3_login_ui
    类初始化参数:
        config_path:类依赖配置文件路径
        driver:driver实例，非必填，不传时，自动创建实例（基础，不包含任何设置的实例）
    -类方法:login_tms
        入参:
        app_name:应用名称[测评，360...]
        username:邮箱
        password:密码
        返回参数: 带cookie的driver实例
    配置文件依赖节点:
        [environment_data] 环境节点
            environment = test 或 prod

interface登陆接口 v3_login_interface:

    引用路径: from v3_components.page.login import v3_login_interface
    类无初始化参数
    类方法:login_tms
        入参:
        environment:环境
        username:邮箱
        password:密码
---
v5_components:
=
italent UI 登陆 login

    引用路径: from v5_components.page.module import login
    入参:
        environment:环境
        username:邮箱
        password:密码
        driver:driver实例
    无返回参数
italent_interface 登陆 login_interface

    引用路径: from v5_components.page.module import login_interface
    入参:
        environment:环境
        username:邮箱
        password:密码
    返回:带cookie的session
italent UI 代办处理 unfinished_transactions

    引用路径: from v5_components.page.module import unfinished_transactions
    入参:
        driver:driver实例
        environment:环境link|cn
        transaction_type: 产品名称[绩效管理、测评中心、人才模型]
        transaction_name: 活动名称
        subtitle 待办的副标题，默认不填写
    无返回参数:UI进行页面跳转至待办链接
切换菜单 go_to_menu

    引用路径: from v5_components.page.module import go_to_menu
    入参:
        driver:driver实例
        environment:环境
        menu_name:菜单名称
    无返回参数:UI进行页面跳转至对应用页面
    菜单名称与链接的映射由远程文件控制，地址:http://8.141.50.128/static/json_data/menu_mapping.json


获取页面产生的fromview的最后一个请求中的字段数据 get_form_view

    引用路径: from v5_components.page.module import get_form_view
    入参
        driver:driver实例
    返回参数:一个包含字典的list集合
                list[{
                    'cmp_id': 'cmp_id',
                    'cmp_label': 'cmp_label',
                    'cmp_name': 'cmp_name',
                    'cmp_type': 'cmp_type',
                    'cmp_data': 'cmp_data'
                }]
操作表单方法，自动填充所有传入的的字段 option_form

    引用路径: from v5_components.page.module import option_form
    入参:
        driver: driver实例
        need_operate_fields: 指定需要操作的字段，字段格式，例如 {'单选框-是否':'是','单选框-单选框':'飞机'}
    无返回参数：对应页面的表单自动填充

对筛选条件进行操作,支持常用筛选和高级筛选，默认为常用筛选 filter_item

    引用路径: from v5_components.page.module import filter_item
    入参: 例如：filter_item(web_driver_initialize, "文本框-人员单选",['管理员'],oper_type='advanced')
        driver: driver实例
        filter_name: 筛选条件的名称，如果有相同名称的筛选条件，使用->符号来确定是第几个，例如‘名称->2’取筛选条件里第2个名称
        content: 筛选内容，可以不填
        oper_type: 筛选类型，分为高级筛选项、常用筛选项，常用筛选项就是直接展示在筛选区域的，高级筛选项是需要点击“高级筛选”后在高级筛选区域进行选择操作
    默认为常用筛选项
    无返回参数: 调用此方法，对筛选条件进行输入、勾选、选择操作

点击列表复选框 click_check_index

    引用路径: from v5_components.page.module import click_check_index
    入参:
        driver: driver实例
        list_index: 列表复选框的顺序， 可以是一个int，也可以是一个list， 
        
    无返回参数: 调用此方法，列表中对应传入的位置的复选框被点击

点击视图区域的按钮
    
    引用路径: from v5_components.page.module import view_button_click
    入参:
        driver: driver实例
        button_name：按钮的text值，即按钮名称 
        
    无返回参数: 调用此方法，点击视图区域功能按钮中对应名称的值

点击列表区域的按钮
    
    引用路径: from v5_components.page.module import list_button_click
    入参:
        driver: driver实例
        button_name：按钮的text值，即按钮名称 
        
    无返回参数: 调用此方法，点击列表页面功能按钮中对应名称的值


获取弹窗列表数据操作
    
    引用路径: from v5_components.page.module import get_form_list_info
    入参:
        driver: driver实例
        
    无返回参数: 调用此方法，获取勾选列表弹窗的列表数据

勾选列表弹窗的数据操作
    
    引用路径: from v5_components.page.module import form_list_operation
    入参:
        driver: driver实例
        kwargs: {'字段名称':'字段值'}例如：字典{'TypeId':1} 勾选TypeId字段为1的数据；不传该参数，默认勾选第一条

    无返回参数: 调用此方法，勾选列表弹窗中对应的符合要求的数据

对字段cmp_type=BC_DigitText的字段进行操作 bc_digit_text_operation
    
    引用路径: from v5_components.page.module import bc_digit_text_operation
    入参:
        driver: driver实例
        field: 字段信息，用于判断是整数还是小数
        input_element: 输入框的element元素
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_DigitText进行填写

对字段cmp_type=BC_TextBoxRange的字段进行操作 bc_text_box_range_operation
    
    引用路径: from v5_components.page.module import bc_text_box_range_operation
    入参:
        driver: driver实例
        field: 字段信息，用于判断是整数还是小数
        input_elements: 输入框的element,2个
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_TextBoxRange进行填写

对字段cmp_type=BC_Email的字段进行操作 bc_email_operation
    
    引用路径: from v5_components.page.module import bc_email_operation
    入参:
        driver: driver实例
        input_element: 输入框的element
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_Email进行填写

对字段cmp_type=BC_Formula的字段进行操作 bc_formula_operation
    
    引用路径: from v5_components.page.module import bc_formula_operation
    入参:
        driver: driver实例
        input_element: 输入框的element
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_Formula进行填写

对字段cmp_type=BC_TextBox的字段进行操作 bc_text_box_operation
    
    引用路径: from v5_components.page.module import bc_text_box_operation
    入参:
        driver: driver实例
        input_element: 输入框的element
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_TextBox进行填写

对字段cmp_type=BC_Url的字段进行操作 bc_url_operation
    
    引用路径: from v5_components.page.module import bc_url_operation
    入参:
        driver: driver实例
        input_element: 输入框的element
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_Url进行填写

对字段cmp_type=BC_LookUpV2的字段进行操作 bc_look_up_v2_operation
    
    引用路径: from v5_components.page.module import bc_look_up_v2_operation
    入参:
        driver: driver实例
        content: 输入框自定义的填写，可以不填为None
        
    无返回参数: 调用此方法，对BC_LookUpV2进行填写

对字段cmp_type=BC_SingleDepartment\BC_PopTree的字段进行操作 bc_single_department_operation
    
    引用路径: from v5_components.page.module import bc_single_department_operation
    入参:
        driver: driver实例
        content: 输入框自定义的填写，默认选择第一个部门
        
    无返回参数: 调用此方法，对BC_SingleDepartment\BC_PopTree进行填写

对字段cmp_type=BC_userSelect的字段进行操作 bc_user_select_operation
    
    引用路径: from v5_components.page.module import bc_user_select_operation
    入参:
        driver: driver实例
        nput_element: 输入框的element元素
        content: 输入框自定义的填写，默认选择第一个人员
        
    无返回参数: 调用此方法，对BC_userSelect进行填写

对字段cmp_type=BC_TextArea、BC_TextAreaRTF的字段进行操作 bc_textarea_operation
    
    引用路径: from v5_components.page.module import bc_textarea_operation
    入参:
        driver: driver实例
        input_element: 输入框的element元素
        content: 输入框自定义的填写，默认选择第一个人员
        
    无返回参数: 调用此方法，对BC_TextArea、BC_TextAreaRTF进行填写

对字段cmp_type=BC_RadioList的字段进行操作 bc_radio_list_operation
    
    引用路径: from v5_components.page.module import bc_radio_list_operation
    入参:
        item_element:单选文字区域
        content: 选项名称
        
    无返回参数: 调用此方法，对BC_RadioList进行填写

对字段cmp_type=BC_DropDownList的字段进行操作 bc_drop_down_list_operation
    
    引用路径: from v5_components.page.module import bc_drop_down_list_operation
    入参:
        driver: driver实例
        field:判断是否为多选、单选
        content: 选项名称
        
    无返回参数: 调用此方法，对BC_DropDownList进行填写

对字段cmp_type=BC_DateTime\BC_Time的字段进行操作 bc_date_time_operation
    
    引用路径: from v5_components.page.module import bc_date_time_operation
    入参:
        driver: driver实例
        field: 字段信息
        input_element: 日期输入框元素
        content: 日期输入内容
        
    无返回参数: 调用此方法，对BC_DateTime\BC_Time进行填写

对字段cmp_type=BC_PictureUploader, BC_FileUploader的字段进行操作 bc_picture_and_file_uploader_operation
    
    引用路径: from v5_components.page.module import bc_picture_and_file_uploader_operation
    入参:
        driver: driver实例
        field: 字段信息
        input_element: 日期输入框元素
        content: 日期输入内容，传入上传文件的地址，不传时，会去case_data中取upload_file中配置的文件路径
        
    无返回参数: 调用此方法，对BC_PictureUploader, BC_FileUploader进行填写

对字段cmp_type=BC_PopArea的字段进行操作 bc_pop_area_operation
    
    引用路径: from v5_components.page.module import bc_pop_area_operation
    入参:
        driver: driver实例
        field:字段信息，格式例如
        content: 选项名称，格式例如：[['四川省','内江市','威远县'],['天津市','河西区']]
        
    无返回参数: 调用此方法，对BC_PopArea进行填写

对字段cmp_type=BC_DateTimeRange的字段进行操作 bc_date_range_operation
    
    引用路径: from v5_components.page.module import bc_date_range_operation
    入参:
        driver:driver实例
        data_format: 日期格式，支持yyyy/MM/dd HH:mm:ss、yyyy/MM/dd、yyyy/MM、HH:mm
        range_input_elements: 日期输入框的元素
        content: 输入的日期内容，数组形式，比如
        'yyyy/MM/dd HH:mm:ss':"日期时间", ["20210504","20220101"],没有值，默认为“此刻”
        'yyyy/MM/dd':"日期类型", ["20210504","20220101"],没有值，默认为“今天”
        'yyyy/MM':"年月", ["2022/09", "2022/10"],没有值，默认为本月
        'HH:mm':"年月", ['0922','1022']
    无返回参数: 调用此方法，对BC_DateTimeRange进行填写