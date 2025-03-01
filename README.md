## About
test
This is the code for paper "From Hardware Fingerprint to Access Token: Enhancing the Authentication on IoT Devices".
```
@INPROCEEDINGS{MCU_Token,
  author = {Yue Xiao and Yi He and Xiaoli Zhang and Qian Wang and Renjie Xie and Kun Sun and Ke Xu and Qi Li},
 title = {From Hardware Fingerprint to Access Token: Enhancing the Authentication on IoT Devices},
 booktitle = {Network and Distributed Security Symposium (NDSS 2024)},
 year = 2024
}
```

The code is organized as follows:
```
├── Device-porting # code for porting MCU-Token SDK to various IoT devices
└── MCUToken
      ├── iot_client # code for MCU-Token's client SDK which runs on IoT devices to collect hardware fingerprints
      └── server # code for MCU-Token' backend authenticate service
```

"[MCUToken/iot_client/readme.md](MCUToken/iot_client/readme.md)" is a code document that describes some important code fragments.   

The authors' contacts are:
```
2365532856@qq.com
clangllvm@126.com
```

## Tips for Artifact Evaluation (and Reproduction) 

1. Run MCU-Token  

Please refer to "[Device-porting/readme.md](Device-porting/readme.md)" to see how to run MCU-Token.  
This step may require 30min.  

2. Reproduce the results in the paper  

Please refer to "[MCUToken/server/evaluation/readme.md](MCUToken/server/evaluation/readme.md)" to reproduce the results in the paper using the logs (training results) we provide.

Please refer to "[MCUToken/server/readme.md](MCUToken/server/readme.md)" to learn more about how to collect data from devices and generate training results by yourself.
