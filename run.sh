#!/bin/bash

echo RUN base model MI_net on dataset elephant
python main_ban.py MI_net --dataset=elephant --model=MI_net
echo RUN base model attnet on dataset elephant 
python main_ban.py attnet --dataset=elephant --model=attnet
echo RUN base model sa_abmilp on dataset elephant 
python main_ban.py sa_abmilp --dataset=elephant --model=sa_abmilp

echo RUN base model MI_net on dataset fox 
python main_ban.py MI_net --dataset=fox --model=MI_net
echo RUN base model attnet on dataset fox 
python main_ban.py attnet --dataset=fox --model=attnet
echo RUN base model sa_abmilp on dataset fox 
python main_ban.py sa_abmilp --dataset=fox --model=sa_abmilp

echo RUN base model MI_net on dataset tiger 
python main_ban.py MI_net --dataset=tiger --model=MI_net
echo RUN base model attnet on dataset tiger 
python main_ban.py attnet --dataset=tiger --model=attnet
echo RUN base model sa_abmilp on dataset tiger 
python main_ban.py sa_abmilp --dataset=tiger --model=sa_abmilp

echo RUN base model MI_net on dataset musk1 
python main_ban.py MI_net --dataset=musk1 --model=MI_net
echo RUN base model attnet on dataset musk1 
python main_ban.py attnet --dataset=musk1 --model=attnet
echo RUN base model sa_abmilp on dataset musk1 
python main_ban.py sa_abmilp --dataset=musk1 --model=sa_abmilp

echo RUN base model MI_net on dataset musk2 
python main_ban.py MI_net --dataset=musk2 --model=MI_net
echo RUN base model attnet on dataset musk2 
python main_ban.py attnet --dataset=musk2 --model=attnet
echo RUN base model sa_abmilp on dataset musk2 
python main_ban.py sa_abmilp --dataset=musk2 --model=sa_abmilp

echo RUN base model MI_net on dataset messidor 
python main_ban.py MI_net --dataset=messidor --model=MI_net
echo RUN base model attnet on dataset messidor 
python main_ban.py attnet --dataset=messidor --model=attnet
echo RUN base model sa_abmilp on dataset messidor
python main_ban.py sa_abmilp --dataset=messidor --model=sa_abmilp