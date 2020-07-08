import datetime


# Обертки сервисов
class Wrapper1C:
    def __init__(self, name_object, object_to_serial):

        value = ""
        type = ""
        if name_object == "ПлатежноеПоручение":
            name_object_type = Operation.get_name_type_payment(self, object_to_serial)
            if name_object_type == "in":
                value_object = PaymentOrderIn(object_to_serial)
            elif name_object_type == "out":
                value_object = PaymentOrderOut(object_to_serial)
            value = value_object.value
        if value != "":
            self.value = {
                "#type": value_object.typeObject1C + "." + value_object.nameType,
                "#value": value
            }
        else:
            self.value = ""


class WrapperTinkoff:
    def __init__(self, name_object, object_to_serial):
        if name_object == "Operation":
            pass
        self.value = ""


# Объекты внешних ИС
class Operation:
    def __init__(self, operation_type):
        self.operationType = operation_type
        self.kbk = "kbk_test"
        self.payerInn = "payerInn"
        self.payerKpp = "payerKpp"
        self.payerName = "payerName"
        self.amount = 123
        self.recipient = "test",
        self.recipientInn = "test",
        self.recipientKpp = "test",
        self.payerAccount = "test",
        self.payerCorrAccount = "test",
        self.payerBank = "test",
        self.payerBic = "test",
        self.recipientAccount = "test",
        self.recipientCorrAccount = "test",
        self.recipientBank = "test",
        self.recipientBic = "test",
        self.id = "123",
        self.paymentType = "test",
        self.uin = "test",
        self.creatorStatus = "test",
        self.oktmo = "test",
        self.taxEvidence = "test",
        self.taxPeriod = "test",
        self.taxDocNumber = "test",
        self.taxDocDate = "test",
        self.taxType = "test",
        self.executionOrder = "test"

    @staticmethod
    def get_name_type_payment(self, operation):
        if operation.operationType == "":
            return "in"
        else:
            return "out"


# Объекты конфигурации 1С
class Object1c():
    def __init__(self):
        self.value = {
            "Ref": "00000000-0000-0000-0000-000000000000",
            "DeletionMark": False
        }
        self.nameType = "te"
        self.typeObject1C = ""


class Document1c(Object1c):
    def __init__(self):
        Object1c.__init__(self)
        self.value.update({
            "Date": str(datetime.datetime.now()),
            "Number": "",
            "Posted": False
        })
        self.nameType = ""
        self.typeObject1C = "jcfg:DocumentObject"


# Объекты метаданных 1С
class PaymentOrder(Document1c):
    def __init__(self, operation):
        Document1c.__init__(self)
        self.value.update({
            "ВалютаДокумента": get_link_object_1c(self, "currency",
                                                  {"КодВалюты": 643}),
            "ВидОперации": operation.operationType,
            "Контрагент": get_link_object_1c(self, "client",
                                             {"ИНН": operation.payerInn,
                                              "КПП": operation.payerKpp,
                                              "Наименование": operation.payerName}),
            "Организация": get_link_object_1c(self, "company",
                                              {"Наименование": operation.recipient,
                                               "ИНН": operation.recipientInn,
                                               "КПП": operation.recipientKpp}),
            "Ответственный": "",
            "ОтражатьВБухгалтерскомУчете": True,
            "ОтражатьВНалоговомУчете": True,
            "ОтраженоВОперУчете": True,
            "Подразделение": "",
            "Комментарий": operation.id,
            "СуммаДокумента": operation.amount,
            "СчетКонтрагента": get_link_object_1c(self, "clientAccount",
                                                  {"НомерСчета": operation.payerAccount,
                                                   "КорСчет": operation.payerCorrAccount,
                                                   "БАНК": operation.payerBank,
                                                   "БИК": operation.payerBic}),
            "СчетОрганизации": get_link_object_1c(self, "companyAccount",
                                                  {"НомерСчета": operation.recipientAccount,
                                                   "КорСчет": operation.recipientCorrAccount,
                                                   "БАНК": operation.recipientBank,
                                                   "БИК": operation.recipientBic}),
        })

    @staticmethod
    def get_name_type_payment(self, document1C):
        if document1C.nameType == "jcfg:DocumentObject.ПлатежноеПоручениеВходящее":
            return "in"
        else:
            return "out"

    @staticmethod
    def set_value(self, document1c, name_value, value):
        document1c.value.update({name_value: value})


class PaymentOrderIn(PaymentOrder):
    def __init__(self, operation):
        PaymentOrder.__init__(self, operation)
        self.value.update({'КодКБК': operation.kbk})
        self.nameType = "ПлатежноеПоручениеИсходящее"


class PaymentOrderOut(PaymentOrder):
    def __init__(self, operation):
        PaymentOrder.__init__(self, operation)
        self.value.update({'ППВ': operation.kbk})
        self.nameType = "ПлатежноеПоручениеВходящее"


# Получение ссылок из 1С
def get_link_object_1c(self, object_1c, parameters_request):
    request_1c = ""
    it_test = True

    if it_test:
        body_request = {"request_1c": request_1c, "parameters_request": parameters_request}
        return body_request

    if object_1c == "client":
        template = 'SELECT value FROM z_keyvalue WHERE key=:key'
        parameters = {'key': 'CLIENT_REQUEST'}
        request_1c = session.execute(template, parameters).fetchall()
    else:
        request_1c = ""
    body_request = {"request_1c": request_1c, "parameters_request": parameters_request}

    conn = outgoing.plain_http['mak01.outconn'].conn
    dl_period = 1  # in days

    params = body_request
    response = conn.get(self.cid, params=params)
    if response.status_code != 200:
        return ""
    else:
        data_base = response.json()
        return data_base.link


# Тесты
opertest = Operation("test_value");
testWrapper = Wrapper1C("ПлатежноеПоручение", opertest)

print(testWrapper.value)
