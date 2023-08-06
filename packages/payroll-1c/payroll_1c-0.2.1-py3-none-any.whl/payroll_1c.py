import math

from xml.etree import ElementTree


class Payroll1C:
    def __init__(self, source=None, *, fromstring=None, check=True):
        assert bool(source) is not bool(fromstring)
        if source:
            if fromstring:
                raise ValueError('Used source and fromstring arguments together')
            self.root = ElementTree.parse(source).getroot()
        elif fromstring:
            self.root = ElementTree.fromstring(fromstring)
        else:
            raise ValueError('Empty source and fromstring arguments')

        assert self.root.tag == 'СчетаПК'

        self.payrolls = self.root[0]
        assert self.payrolls.tag == 'ЗачислениеЗарплаты'

        if check:
            self.check()

    def check(self):
        total_amount = 0
        sequence_number = 0
        for employee in self.payrolls:
            sequence_number += 1
            if int(employee.get('Нпп')) != sequence_number:
                raise ValueError('Incorrect Employee element sequence number attribute value')
            total_amount += float(employee.find('Сумма').text)

        checksums = self.root[1]
        assert checksums.tag == 'КонтрольныеСуммы'

        employee_count = int(checksums.find('КоличествоЗаписей').text)
        if employee_count != sequence_number:
            raise ValueError('Incorrect Employee record count')

        total_amount_checksum = float(checksums.find('СуммаИтого').text)
        if not math.isclose(total_amount, total_amount_checksum, abs_tol=0.001):
            raise ValueError('Incorrect total amount checksum')

    def __getitem__(self, item):
        return self.root.get(item)

    def attrs(self):
        return self.root.attrib

    def __iter__(self):
        for employee in self.payrolls:
            employee_dict = {employee_child.tag: employee_child.text for employee_child in employee}
            employee_dict['Сумма'] = float(employee_dict['Сумма'])
            yield employee_dict
