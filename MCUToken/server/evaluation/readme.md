### MCU-Token Experiments

We will explain how to generate the key figures and tables from the logs we provide.

#### Prepare

Python Environment, we suggest you use Anaconda to create and manage your environment.

```bash
# get conda
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

# creat Python with conda, for example
conda create -n py38 python=3.8

# activate python
conda activate py38
```

You should make sure that you already have the necessary packages installed.

```bash
$ cd ..
$ pip install -r requirements.txt
$ cd evaluation
```
#### Figure 2 (Attack Example on IoT-ID)

Run the following commands, which will produce Figure 2 (picture/Fig-2a.pdf && picture/Fig-2b.pdf).

```bash
$ cd plot && python Fig-2_plot.py
```

#### Figure 5 (Fingerprint Example)

Run the following commands, which will produce Figure 5 (picture/Fig-5a.pdf && picture/Fig-5b.pdf).

```bash
$ cd plot && python Fig-5_plot.py
```

#### Table III (Authentication Results)

Run the following commands, which will print Table III.

```bash
$ cd plot && python Tab-3_show.py
```

#### Figure 6 (Environment Evaluation)

Run the following commands, which will produce Figure 6 (picture/Fig-6.pdf).

```bash
$ cd plot && python Fig-6_plot.py
```

#### Figure 7 (Authentication Results with Different Parameters)

Run the following commands, which will produce Figure 7 (picture/Fig-7a.pdf && picture/Fig-7b.pdf).

```bash
$ cd plot && python Fig-7_plot.py
```

#### Figure 8 (Authentication of Poisoned Fingerprints)

Run the following commands, which will produce Figure 8(picture/Fig-8.pdf).

```bash
$ cd plot && python Fig-8_plot.py
```

#### Table IV (Hardware Mimic Attack Evaluation)

Run the following commands, which will print Table IV.

```bash
$ cd plot && python Tab-4_show.py
```

#### Figure 9 (Software Mimic Attack Evaluation)

Run the following commands, which will produce Figure 9 (picture/Fig-9a.pdf && picture/Fig-9b.pdf && picture/Fig-9c.pdf).

```bash
$ cd plot && python Fig-9_plot.py
```

#### Figure 10 (Software Mimic Attack Evaluation on Single Fingerprints)

Run the following commands, which will produce Figure 10 (picture/Fig-10a.pdf && picture/Fig-10b.pdf && picture/Fig-10c.pdf && picture/Fig-10d.pdf).

```bash
$ cd plot && python Fig-10_plot.py
```

#### Figure 11 (Tampering Attack Evaluation)

Run the following commands, which will produce Figure 11 (picture/Fig-11a.pdf && picture/Fig-11b.pdf).

```bash
$ cd plot && python Fig-11_plot.py
```

#### Table V (Evaluation on Identification of Attackers)

Run the following commands, which will print Table V.

```bash
$ cd plot && python Tab-5_show.py
```
