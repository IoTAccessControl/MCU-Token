sh 1_Fig-2.sh > ./result_cmp/Fig-2_log 
sh 2_Tab-3_esp32_single.sh > ./result_cmp/Tab-3_esp32_all_log 
python auth.py --repeat_time 20 --device_number 30 --all_data 0 --device_type esp32 --multiple_only 0 > ./result_cmp/Tab-3_esp32_part_log 
sh 2_Tab-3_f103_single.sh > ./result_cmp/Tab-3_f103_all_log 
python auth.py --repeat_time 20 --device_number 20 --all_data 0 --device_type stm32f103 --multiple_only 0 > ./result_cmp/Tab-3_f103_part_log 
sh 2_Tab-3_f429_single.sh > ./result_cmp/Tab-3_f429_all_log 
python auth.py --repeat_time 20 --device_number 10 --all_data 0 --device_type stm32f429 --multiple_only 0 > ./result_cmp/Tab-3_f429_part_log 
sh 3_Fig-6.sh > ./result_cmp/Fig-6_log 
sh 4_Fig-7a.sh > ./result_cmp/Fig-7a_log 
sh 4_Fig-7b.sh > ./result_cmp/Fig-7b_log 
python attack_hardware_mimic.py --source_device esp32 --repeat_time 20 > ./result_cmp/Tab-4_log/esp32_0 
python attack_hardware_mimic.py --source_device stm32 --repeat_time 20 > ./result_cmp/Tab-4_log/f429_0
python attack_hardware_mimic.py --source_device stm32f103 --repeat_time 20 > ./result_cmp/Tab-4_log/f103_0 
sh 6_Fig-8.sh > ./result_cmp/Fig-8_log 
sh 7_Fig-9a.sh > ./result_cmp/Fig-9a_log 
sh 7_Fig-9b.sh > ./result_cmp/Fig-9b_log 
sh 7_Fig-9c.sh > ./result_cmp/Fig-9c_log 
sh 8_Fig-10a.sh > ./result_cmp/Fig-10a_log 
sh 8_Fig-10b.sh > ./result_cmp/Fig-10b_log 
sh 8_Fig-10c.sh > ./result_cmp/Fig-10c_log 
sh 8_Fig-10d.sh > ./result_cmp/Fig-10d_log 
sh 9_Tab-5.sh > ./result_cmp/Tab-5_log 
python attack_tamper.py --test_type 12 --out_len 1000 > ./result_cmp/Fig-11_log/result_1000_12 
python attack_tamper.py --test_type 12 --out_len 5000 > ./result_cmp/Fig-11_log/result_5000_12 
python attack_tamper.py --test_type 12 --out_len 10000 > ./result_cmp/Fig-11_log/result_10000_12 
python attack_tamper.py --test_type 12 --out_len 15000 > ./result_cmp/Fig-11_log/result_15000_12 
python attack_tamper.py --test_type 12 --out_len 20000 > ./result_cmp/Fig-11_log/result_20000_12 
python attack_tamper.py --test_type 1 --out_len 1000 > ./result_cmp/Fig-11_log/result_1000_1 
python attack_tamper.py --test_type 1 --out_len 5000 > ./result_cmp/Fig-11_log/result_5000_1 
python attack_tamper.py --test_type 1 --out_len 10000 > ./result_cmp/Fig-11_log/result_10000_1 
python attack_tamper.py --test_type 1 --out_len 15000 > ./result_cmp/Fig-11_log/result_15000_1 
python attack_tamper.py --test_type 1 --out_len 20000 > ./result_cmp/Fig-11_log/result_20000_1 