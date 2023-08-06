import sys
from qiskit import *
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
import logging
import time
import json
import os
import threading

def ConfigCheck():
    try:
        _qclogger.logger.info("Loading account...")
        IBMQ.load_account()
        _qclogger.logger.info("Account loaded succesfully!")
    except:
        try:
            _qclogger.logger.error("Loading failed! Loading from token.txt")
            token = ""
            with open("token.txt","r") as tokenFile:
                token = tokenFile.readline()
            
            IBMQ.save_account(token)
            IBMQ.load_account()
        except:
            _qclogger.logger.error("Loading from token.txt failed!")

def ChooseBackend(NotASimulator=False):
    try:
        _qclogger.logger.info("Selecting backend...")
        provider = IBMQ.get_provider(hub='ibm-q')
        servers = provider.backends(filters=lambda b: "reset" in b.configuration().basis_gates and not b.configuration().backend_name in _qcconfig.exclusions, simulator=False, operational=True)
        leastbusy = least_busy(servers)
        backend = provider.get_backend("{}".format(leastbusy))
        _qclogger.logger.info("Selected {}!".format(leastbusy))
    except:
        _qclogger.logger.error("Selecting backend failed!")
        if NotASimulator == True:
            backend = "No quantum computer is available"
        else:
            backend = BasicAer.get_backend("qasm_simulator")
    return backend

class _QCLogging:
    def __init__(self):
        self.logger = logging.getLogger('QCLogger')
        self.formatter = logging.Formatter('%(asctime)s: %(levelname)s> %(message)s')
        self.UpdateHandler()
        self.logger.setLevel(logging.DEBUG)
    def UpdateHandler(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        
        if _qcconfig.logFile == 'stdout':
            self.handler = logging.StreamHandler(sys.stdout)
        else:
            self.handler = logging.FileHandler(_qcconfig.logFile)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        
class _QCBackend:
    def __init__(self):
        ConfigCheck()
        self.lastChange = time.time()
        self.backend = ChooseBackend()
    def GetBackend(self):
        if (time.time() - self.lastChange > _qcconfig.expireTime):
            self.backend = ChooseBackend()
            self.lastChange = time.time()
        return self.backend

class _QCConfig:
    def __init__(self):
        self.logFile = 'qcrandom.log'
        self.exclusions = []
        self.expireTime = 600

        self.bufferSize = 100
        self.bufferAccuracy = 64
        self.bufferRefill = 0.5
        self.CreateFile()
        self.LoadConfig()
    
    def CreateFile(self):
        if not os.path.exists("config.json"):
            newFile = {
                "Expire": self.expireTime,
                "Log_File": self.logFile,
                "Exclusions": self.exclusions,

                "Buffer": {
                    "Size": self.bufferSize,
                    "Accuracy": self.bufferAccuracy,
                    "Refill": self.bufferRefill
                }
            }
            with open("config.json", "w") as file:
                file.write(json.dumps(newFile))

    def LoadConfig(self):
        with open("config.json", "r") as file:
            config = json.load(file)
            if 'Log_File' in config:
                self.logFile = config['Log_File']
			
            if 'Exclusions' in config:
                self.exclusions = config['Exclusions']

            if 'Expire' in config:
                self.expireTime = config['Expire']

            if 'Buffer' in config:
                if 'Size' in config['Buffer']:
                    self.bufferSize = config['Buffer']['Size']
                if 'Accuracy' in config['Buffer']:
                    self.bufferAccuracy = config['Buffer']['Accuracy']
                if 'Refill' in config['Buffer']:
                    self.bufferRefill = config['Buffer']['Refill']

_qcconfig = _QCConfig()
_qclogger = _QCLogging()
_qcbackend = _QCBackend()
_qcbuffer = []

def LoadConfig():
    _qcconfig.LoadConfig()
    _qclogger.UpdateHandler()
    

def GetRoundFactor(accuracy):
    return len(str(2**accuracy))

def GenerateBuffer(accuracy, buffersize):
    assert accuracy > 1, "Accuracy must be higher than 1!"
    assert buffersize > 0, "Buffer size must be higher than 0!"

    qr = QuantumRegister(1)
    cr = ClassicalRegister(accuracy)
    circuit = QuantumCircuit(qr, cr)

    for j in range(accuracy):
        circuit.h(0)
        circuit.measure(0, j)
        if j < accuracy - 1:
            circuit.reset(0)

    job = execute(circuit, _qcbackend.GetBackend(), shots=buffersize, memory=True)
    if _qcconfig.logFile == 'stdout':
        job_monitor(job, interval=5, output=sys.stdout)
    else:
        with open(_qcconfig.logFile, 'a') as file:
            file.write(time.asctime())
            job_monitor(job, interval=5, output=file)

    data = job.result().get_memory()

    _qcthreading.buffer.clear()
    for number in data:
        _qcthreading.buffer.append(round(int(number, 2) / (2**accuracy - 1), GetRoundFactor(accuracy)))

def _QCGenerateBuffer():
    GenerateBuffer(_qcconfig.bufferAccuracy, _qcconfig.bufferSize)

class _QCThreading:
    def __init__(self):
        self.thread = threading.Thread(target=_QCGenerateBuffer)
        self.buffer = []
        self.thread.start()
    def newThread(self):
        self.thread = threading.Thread(target=_QCGenerateBuffer)

_qcthreading = _QCThreading()

def CheckBufferState():
    assert _qcconfig.bufferRefill <= 1.0, "Buffer refill threshold must be lower or equal to 1!"
    assert _qcconfig.bufferRefill >= 0, "Buffer refill threshold must be higher or equal to 0!"
    if GetBufferSize() <= _qcconfig.bufferRefill * _qcconfig.bufferSize:
        if not _qcthreading.thread.is_alive() and len(_qcthreading.buffer) == 0:
            _qclogger.logger.info(f"Second thread started working, main buffer size {GetBufferSize()}")
            _qcthreading.newThread()
            _qcthreading.thread.start()
    if GetBufferSize() == 0:
        _qcthreading.thread.join()
        _qcbuffer.extend(_qcthreading.buffer)
        _qcthreading.buffer.clear()

# Generates random number between 0 and 1
def GenerateRandomFraction(accuracy):
    assert accuracy > 1, "Accuracy must be higher than 1!"
    CheckBufferState()
    number = _qcbuffer[0]
    _qcbuffer.pop(0)
    return round(number, GetRoundFactor(accuracy))

def QCRandom(left, right, accuracy=16):
    assert accuracy > 1, "Accuracy must be higher than 1!"
    assert left < right, "Left must be lower than right!"
    
    ret = GenerateRandomFraction(accuracy) * abs(right - left) + left
    return round(ret, GetRoundFactor(accuracy))

def GetBufferSize():
    return len(_qcbuffer)