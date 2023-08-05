from xml.etree import ElementTree

ElementTree.register_namespace('SOAP-ENV', "http://schemas.xmlsoap.org/soap/envelope/")


def modify_dacc_parameters(src_path: str, dest_path: str, *args):
    '''

    :param src_path:
    :param dest_path:
    :param args: (portNumber1, S1, position1, variableDelay1), (portNumber2, S2, position2, variableDelay2),
                 (portNumber3, S3, position3, variableDelay3)
    :return:
    '''
    tree = ElementTree.parse(src_path)
    root = tree.getroot()
    for i, managedObject in enumerate(root.iter('managedObject')):
        managedObject.find("./parameter[parameterName='portNumber']").find('newValue').text = str(args[i][0])
        managedObject.find("./parameter[parameterName='S']").find('newValue').text = str(args[i][1])
        managedObject.find("./parameter[parameterName='position']").find('newValue').text = str(args[i][2])
        managedObject.find("./parameter[parameterName='variableDelay']").find('newValue').text = str(args[i][3])
    tree.write(dest_path)


def modify_freq_bandwidth_power(src_path: str, dest_path: str, *args):
    '''

    :param src_path:
    :param dest_path:
    :param args: (freq1, bw1, pow1), (freq2, bw2, pow2), (freq3, bw3, pow3)
                 如果pow为None，则不对power进行赋值
    :return:
    '''
    tree = ElementTree.parse(src_path)
    root = tree.getroot()
    for i, managedObject in enumerate(root.iter('managedObject')):
        managedObject.find("./parameter[parameterName='channels']").find('newValue').find('channel').find(
            'frequency').text = str(int(args[i][0] * 1e6))
        managedObject.find("./parameter[parameterName='channels']").find('newValue').find('channel').find(
            'bandwidth').text = str(int(args[i][1] * 1e6))
        if args[i][2] is not None:
            managedObject.find("./parameter[parameterName='power']").find('newValue').text = f"{args[i][2]:g}"
    tree.write(dest_path)


def modify_modulationlevel(src_path: str, dest_path: str, enable: bool):
    data_modul = """       <parameter>
                        <parameterName>modulationLevel</parameterName>
                        <newValue>1</newValue>
                        <prevValue/>
                    </parameter>"""
    tree = ElementTree.parse(src_path)
    root = tree.getroot()
    for i, managedObject in enumerate(root.iter('managedObject')):
        modul = managedObject.find("./parameter[parameterName='modulationLevel']")
        if modul is not None and not enable:
            managedObject.remove(modul)
        elif modul is None and enable:
            managedObject.insert(5, ElementTree.fromstring(data_modul))
    tree.write(dest_path)
