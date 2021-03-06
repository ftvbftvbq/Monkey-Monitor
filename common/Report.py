import logging
import re
import math

from common import Pickle, Analysis, CashEmnu as go


class OperateReport:
    def __init__(self, wd):
        self.wd = wd
        self._crashM = []
        # self.pie(self.wd, worksheet)

    def monitor(self, info):
        worksheet = self.wd.add_worksheet("Analysis")
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 10)
        worksheet.set_column("C:C", 10)
        worksheet.set_column("D:D", 10)
        worksheet.set_column("E:E", 10)
        worksheet.set_column("F:F", 10)
        worksheet.set_column("G:G", 10)
        worksheet.set_column("H:H", 10)
        worksheet.set_column("I:I", 10)
        worksheet.set_column("J:J", 10)
        worksheet.set_column("K:K", 10)
        worksheet.set_column("L:L", 10)
        worksheet.set_column("L:L", 10)
        worksheet.set_column("M:M", 10)
        worksheet.set_column("N:N", 10)
        worksheet.set_column("O:O", 10)
        worksheet.set_column("P:P", 10)
        worksheet.set_column("Q:Q", 10)
        worksheet.set_column("R:R", 10)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)
        worksheet.set_row(10, 30)
        worksheet.set_row(11, 30)
        worksheet.set_row(12, 30)

        define_format_H1 = get_format(self.wd, {'bold': True, 'font_size': 18})
        define_format_H2 = get_format(self.wd, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)

        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("blue")
        define_format_H2.set_color("#ffffff")
        worksheet.merge_range('A1:Q1', 'monkey性能监控', define_format_H1)
        _write_center(worksheet, "A2", '设备名', self.wd)
        _write_center(worksheet, "B2", 'CPU', self.wd)
        _write_center(worksheet, "C2", '内存', self.wd)
        _write_center(worksheet, "D2", '分辨率', self.wd)
        _write_center(worksheet, "E2", "耗时", self.wd)
        _write_center(worksheet, "F2", "CPU峰值", self.wd)
        _write_center(worksheet, "G2", "CPU均值", self.wd)
        _write_center(worksheet, "H2", "内存峰值", self.wd)
        _write_center(worksheet, "I2", "内存均值", self.wd)
        _write_center(worksheet, "J2", "fps峰值", self.wd)
        _write_center(worksheet, "K2", "fps均值", self.wd)
        _write_center(worksheet, "L2", "电量测试之前", self.wd)
        _write_center(worksheet, "M2", "电量测试之后", self.wd)
        _write_center(worksheet, "N2", "上行流量峰值", self.wd)
        _write_center(worksheet, "O2", "上行流量均值", self.wd)
        _write_center(worksheet, "P2", "下行流量峰值", self.wd)
        _write_center(worksheet, "Q2", "下行流量均值", self.wd)

        temp = 3
        for t in info:
            for wrap in t:
                for item in t[wrap]:
                    self.get_crash_msg(t[wrap]["header"]["monkey_log"])
                    _write_center(worksheet, "A" + str(temp), t[wrap]["header"]["phone_name"], self.wd)
                    _write_center(worksheet, "B" + str(temp), t[wrap]["header"]["kel"], self.wd)
                    _write_center(worksheet, "C" + str(temp), str(math.ceil(t[wrap]["header"]["rom"] / 1024)) + "M", self.wd)
                    _write_center(worksheet, "D" + str(temp), t[wrap]["header"]["pix"], self.wd)
                    _write_center(worksheet, "E" + str(temp), t[wrap]["header"]["time"], self.wd)

                    cpu = Pickle.read_info(t[wrap]["cpu"])
                    men = Pickle.read_info(t[wrap]["men"])
                    fps = Pickle.read_info(t[wrap]["fps"])
                    flow = Pickle.read_info(t[wrap]["flow"])
                    _write_center(worksheet, "F" + str(temp), Analysis.max_cpu(cpu), self.wd)
                    _write_center(worksheet, "G" + str(temp), Analysis.avg_cpu(cpu), self.wd)
                    _write_center(worksheet, "H" + str(temp), Analysis.max_men(men), self.wd)
                    _write_center(worksheet, "I" + str(temp), Analysis.avg_men(men), self.wd)
                    _write_center(worksheet, "J" + str(temp), Analysis.max_fps(fps), self.wd)
                    _write_center(worksheet, "K" + str(temp), Analysis.avg_fps(fps), self.wd)
                    _write_center(worksheet, "L" + str(temp), t[wrap]["header"]["beforeBattery"], self.wd)
                    _write_center(worksheet, "M" + str(temp), t[wrap]["header"]["afterBattery"], self.wd)
                    _maxFlow = Analysis.max_flow(flow)
                    _avgFLow = Analysis.avg_flow(flow)
                    _write_center(worksheet, "N" + str(temp), _maxFlow[0], self.wd)
                    _write_center(worksheet, "O" + str(temp), _maxFlow[1], self.wd)
                    _write_center(worksheet, "P" + str(temp), _avgFLow[1], self.wd)
                    _write_center(worksheet, "Q" + str(temp), _avgFLow[1], self.wd)

                    break
                temp = temp + 1

    def get_crash_msg(self, log):
        with open(log, encoding="utf-8") as monkey_log:
            lines = monkey_log.readlines()
            for line in lines:
                if re.findall(go.ANR, line):
                    logging.debug(line)
                    logging.info("存在anr错误:" + line)
                    self._crashM.append(line)
                if re.findall(go.CRASH, line):
                    logging.debug(line)
                    logging.info("存在crash错误:" + line)
                    self._crashM.append(line)
                if re.findall(go.EXCEPTION, line):
                    logging.debug(line)
                    logging.info("存在crash错误:" + line)
                    self._crashM.append(line)
            monkey_log.close()

    def crash(self):
        if len(self._crashM):
            worksheet = self.wd.add_worksheet("crash")
            _write_center(worksheet, "A1", '崩溃统计日志', self.wd)
            temp = 2
            logging.debug(self._crashM)
            for item in self._crashM:
                _write_center(worksheet, "A" + str(temp), item, self.wd)
                temp = temp + 1

    def plot(self, worksheet, types, lenData, name, num):
        """
        :param worksheet:
        :param types: cpu,fps,flow,battery
        :param lenData: 数据长度
        :param name: sheet名字
        :return:
        """
        values = ""
        row = ""
        title = ""
        if types == "cpu":
            values = "=" + name + "!$A$1:$A$" + str(lenData + 1)
            row = 'H2'
            title = "CPU使用率"
        elif types == "men":
            values = "=" + name + "!$B$1:$B$" + str(lenData + 1)
            row = 'H11'
            title = "内存使用MB"
        elif types == "fps":
            values = "=" + name + "!$C$1:$C$" + str(lenData + 1)
            row = 'H27'
            title = "FPS使用情况"
        elif types == "battery":
            values = "=" + name + "!$D$1:$D$" + str(lenData + 1)
            row = 'H43'
            title = "电池剩余%"
        elif types == "flowUp":
            values = "=" + name + "!$E$1:$E$" + str(lenData + 1)
            row = 'H59'
            title = "上行流量KB"
        elif types == "flowDown":
            values = "=" + name + "!$F$1:$F$" + str(lenData + 1)
            row = 'H76'
            title = "下行流量KB"
        chart1 = self.wd.add_chart({'type': 'line'})
        chart1.add_series({
            'values': values
        })
        width = num*10
        if width <= 450:
            width = 450
        elif width >= 1600:
            width = 1600
        chart1.set_size({'width': width})
        chart1.set_title({'name': title})
        # worksheet.insert_chart('A9', chart1, {'x_offset': 2, 'y_offset': 2})
        worksheet.insert_chart(row, chart1)

    def close(self):
        self.wd.close()

    def analysis(self, info):
        for t in info:
            for wrap in t:
                name = wrap.split(':')[0] + "detail" # sheet名字
                worksheet = self.wd.add_worksheet(name)
                worksheet.set_column("A:A", 10)
                worksheet.set_column("B:B", 10)
                worksheet.set_column("C:C", 10)
                worksheet.set_column("D:D", 10)
                worksheet.set_column("E:E", 10)
                worksheet.set_column("F:F", 10)

                worksheet.set_row(1, 30)
                worksheet.set_row(2, 30)
                worksheet.set_row(3, 30)
                worksheet.set_row(4, 30)
                worksheet.set_row(5, 30)
                worksheet.set_row(6, 30)
                define_format_h1 = get_format(self.wd, {'bold': True, 'font_size': 18})
                define_format_h2 = get_format(self.wd, {'bold': True, 'font_size': 14})
                define_format_h1.set_border(1)

                define_format_h2.set_border(1)
                define_format_h1.set_align("center")
                define_format_h2.set_align("center")
                define_format_h2.set_bg_color("blue")
                define_format_h2.set_color("#ffffff")

                _write_center(worksheet, "A1", 'cpu(%)', self.wd)
                _write_center(worksheet, "B1", 'men(M)', self.wd)
                _write_center(worksheet, "C1", 'fps', self.wd)
                _write_center(worksheet, "D1", 'battery(%)', self.wd)
                _write_center(worksheet, "E1", '上行流量(KB)', self.wd)
                _write_center(worksheet, "F1", '下行流量(KB)', self.wd)
                for item in t[wrap]:
                    logging.info("------data-----")
                    temp = 2
                    cpu = Pickle.read_info(t[wrap]["cpu"])
                    for item in cpu:
                        _write_center(worksheet, "A" + str(temp), float("%.2f" % item), self.wd)
                        temp = temp + 1

                    temp = 2
                    men = Pickle.read_info(t[wrap]["men"])
                    for item in men:
                        _write_center(worksheet, "B" + str(temp), math.ceil(item/1024), self.wd)
                        temp = temp + 1

                    temp = 2
                    fps = Pickle.read_info(t[wrap]["fps"])
                    for item in fps:
                        _write_center(worksheet, "C" + str(temp), item, self.wd)
                        temp = temp + 1

                    temp = 2
                    battery = Pickle.read_info(t[wrap]["battery"])
                    for item in battery:
                        _write_center(worksheet, "D" + str(temp), item, self.wd)
                        temp = temp + 1

                    temp = 2
                    flow = Pickle.read_info(t[wrap]["flow"])
                    for item in flow[0]:
                        if item > 0:
                            _write_center(worksheet, "E" + str(temp), math.ceil(item/1024), self.wd)
                        else:
                            _write_center(worksheet, "E" + str(temp), 0, self.wd)
                        temp = temp + 1

                    temp = 2
                    for item in flow[1]:
                        if item > 0:
                            _write_center(worksheet, "F" + str(temp), math.ceil(item/1024), self.wd)
                        else:
                            _write_center(worksheet, "F" + str(temp), 0, self.wd)
                        temp = temp + 1
                    self.plot(worksheet, "cpu", len(cpu), name, t[wrap]["num"])
                    self.plot(worksheet, "men", len(men), name, t[wrap]["num"])
                    self.plot(worksheet, "battery", len(battery), name, t[wrap]["num"])
                    self.plot(worksheet, "fps", len(fps), name, t[wrap]["num"])
                    self.plot(worksheet, "flowUp", len(flow[0]), name, t[wrap]["num"])
                    self.plot(worksheet, "flowDown", len(flow[1]), name, t[wrap]["num"])
                    break


def get_format(wd, option={}):
    return wd.add_format(option)


def get_format_center(wd, num=1):
    return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})


def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)


def _write_center(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_center(wd))


def set_row(worksheet, num, height):
    worksheet.set_row(num, height)


# if __name__ == '__main__':
#     workbook = xlsxwriter.Workbook('报告.xlsx')  # 建立文件
#     info = [
#         {
#             'DU2TAN15AJ049163':
#                 {
#                     'cpu': 'H:\\project\\monkey_report\\info\\EAROU8VOSKAM99I7_cpu.pickle',
#                     'battery': 'H:\\project\\monkey_report\\info\\EAROU8VOSKAM99I7_battery.pickle',
#                     'men': 'H:\\project\\monkey_report\\info\\EAROU8VOSKAM99I7_men.pickle',
#                     'flow': 'H:\\project\\monkey_report\\info\\EAROU8VOSKAM99I7_flow.pickle',
#                     'header':
#                         {
#                             'rom': 3085452,
#                             'kel': '8核',
#                             'monkey_log': 'H:\\project\\monkey_report\\monkey.log',
#                             'beforeBattery': 94,
#                             'pix': '1080x1920',
#                             'time': '15秒',
#                             'afterBattery': 94,
#                             'phone_name': 'H60-L02_Huawei_4.4',
#                         },
#                     'num': '200',
#                     'fps': 'H:\\project\\monkey_report\\info\\EAROU8VOSKAM99I7_fps.pickle'
#                 }
#         }
#     ]
#     tem = OperateReport(workbook)
#     tem.monitor(info)
#     tem.analysis(info)
#     tem.crash()
#     tem.close()
#     # print(len(data["cpu"]))
