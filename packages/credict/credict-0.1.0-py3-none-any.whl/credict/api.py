"""
High-level API.
"""
import json
import time
from rich.console import Console
from .encryption import RSA
from .watermark import AddressBasedWatermarker


class SingleContractPredictionHandler:
    PREDICTION_SCHEMA = (
        "target_oracle",
        "target_time",
        "creation_time",
        "predicted_value",
        "is_decrypted",
        "prediction_address",
        "prediction_author",
        "prediction_comment",
    )
    
    def __init__(
        self,
        sender_address,
        contract_dict,
        target_digits=12,
    ):
        self.logger = Console()
        self.sender_address = sender_address
        self.contract_dict = contract_dict
        self.target_digits = target_digits
        self.setup_watermark()
        self.records_to_decrypt = []
    
    @classmethod
    def from_json(cls, path):
        with open(path, "r") as f:
            data_dict = json.load(f)
        handler = cls(
            data_dict["sender_address"],
            data_dict["contract_dict"],
            data_dict["target_digits"],
        )
        
        handler.setup_rsa(**data_dict["rsa_config"])
        handler.records_to_decrypt = data_dict["records_to_decrypt"]
        return handler
        
    def to_json(self, path):
        assert hasattr(self, "rsa"), "missing RSA setup"
        
        data_dict = {
            "sender_address": self.sender_address,
            "contract_dict": self.contract_dict,
            "target_digits": self.target_digits,
            "rsa_config": self.rsa.describe(),
            "records_to_decrypt": self.records_to_decrypt,
        }
        
        with open(path, "w") as f:
            json.dump(data_dict, f)
        
    def connect(self, web3_provider):
        self.w3 = web3_provider
        self.contract = self.w3.eth.contract(
            abi=self.contract_dict["abi"],
            address=self.contract_dict["address"],
        )
        
    def setup_rsa(self, n=None, e=None, d=None):
        if n and e and d:
            self.logger.print("Loading preset RSA.")
            self.rsa = RSA(n, e, d)
        else:
            assert n is None and e is None and d is None
            self.logger.print("Creating RSA from scratch.")
            self.rsa = RSA.given_digits(self.target_digits)
            
    def setup_watermark(self, num_verifications=20):
        self.watermarker = AddressBasedWatermarker(self.sender_address)
        for _ in range(num_verifications):
            _watermark = self.watermarker.create(self.target_digits)
            assert self.watermarker.verify(_watermark)
        
    def make_prediction(self, txn_func, target_time, value, author="", comment=""):
        assert target_time > time.time(), f"invalid target time {target_time}"
        value_str = str(value)
        watermark_len = self.target_digits - 1 - len(value_str)
        assert watermark_len >= 5, f"available watermark length is too low for {value}"
        watermark = self.watermarker.create(watermark_len)
        
        marked_value = int(f"{watermark}0{value}")
        encrypted_value = self.rsa.encrypt(marked_value)
        
        call = self.contract.functions.makePrediction(
            target_time,
            encrypted_value,
            author,
            comment,
        )
        
        transaction_info = txn_func(call)
        
        decryption_info = {
            "target_time": target_time,
            "encrypted_value": encrypted_value,
            "rsa": self.rsa.describe(),
        }
        # TODO: add transaction status check
        self.records_to_decrypt.append(decryption_info)
        
        json_root = f"{self.sender_address}_{self.contract_dict['address']}"
        self.to_json(f"{json_root}.json")
        return transaction_info

    def view_prediction(self):
        pred_list = self.contract.functions.viewPrediction(self.sender_address).call()
        dict_list = []
        schema = self.__class__.PREDICTION_SCHEMA
        for _pred in pred_list:
            _data_dict = {_k: _v for _k, _v in zip(schema, _pred)}
            dict_list.append(_data_dict)
        
        return dict_list
        
    def decrypt_prediction_greedy(self, txn_func):
        # fetch the earliest non-decrypted prediction
        pred_dict_list = self.view_prediction()
        start_time, start_value, start_idx = None, None, None
        for i, _pred in enumerate(pred_dict_list):
            if not _pred["is_decrypted"]:
                start_time = _pred["target_time"]
                start_value = _pred["predicted_value"]
                start_idx = i
            break
        
        # check against locally stored RSA info
        local_first = self.records_to_decrypt[0]
        assert start_time = local_first["target_time"], "target time mismatch"
        assert start_value = local_first["encrypted_value"], "predicted value mismatch"
        
        # find continuous RSA batch
        rsa_d, rsa_n = local_first["rsa"]["d"], local_first["rsa"]["n"]
        pairs_to_decrypt = zip(pred_dict_list[])
        rsa_batch_len = 0
        for _record in self.records_to_decrypt:
            if _record["rsa"]["d"] == rsa_d and _record["rsa"]["n"] == rsa_n:
                rsa_batch_len += 1
            else:
                break
        
        # pair with online records and check
        pred_slice = pred_dict_list[start_idx:(start_idx+rsa_batch_len)]
        record_slice = self.records_to_decrypt[:rsa_batch_len]
        optimal_creation_thresh = 0
        for i, _pred, _record in zip(pred_slice, record_slice):
            assert _pred["target_time"] == _record["target_time"], "target time mismatch"
            assert _pred["predicted_value"] == _record["encrypted_value"], "predicted value mismatch"
            assert _pred["creation_time"] >= optimal_creation_thresh, "creation time misorder"
            optimal_creation_thresh = _pred["creation_time"]
        
        # match using lookup to determine the creation time threshold
        call = self.contract.functions.decryptPrediction(
            rsa_d,
            rsa_n,
            optimal_creation_thresh,
        )
        
        transaction_info = txn_func(call)
        
        # TODO: add transaction status check
        for _ in range(rsa_batch_len):
            self.records_to_decrypt.pop(0)
        
        return transaction_info