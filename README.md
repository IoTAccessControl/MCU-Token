## About

This is the code for paper "From Hardware Fingerprint to Access Token: Enhancing the Authentication on IoT Devices".

```
├── Device-porting # code for porting MCU-Token SDK to various IoT devices
└── MCUToken
      ├── iot_client # code for MCU-Token's client SDK which runs on IoT devices to collect hardware fingerprints
      └── server # code for MCU-Token' backend authenticate service
```

## Tips for Artifact Evaluation  

1. Run MCU-Token  

Please refer to "[Device-porting/readme.md](Device-porting/readme.md)" to see how to run MCU-Token.  
This step may require 30min.  

2. Reproduce the results in the paper  

Please refer to "[MCUToken/server/evaluation/readme.md](MCUToken/server/evaluation/readme.md)" to reproduce the results in the paper using the logs (training results) we provide.

Please refer to "[MCUToken/server/readme.md](MCUToken/server/readme.md)" to learn more about how to collect data from devices and generate training results by yourself.
