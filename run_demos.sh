#!/usr/bin/bash

python pyfortran.py demo/fibonacci.f demo/fibonacci.in
echo "=============================="
python pyfortran.py demo/prime.f demo/prime.in
echo "=============================="
python pyfortran.py demo/fortransit_example_5_src.f
echo "=============================="
python pyfortran.py demo/MatInv.f
echo "=============================="
python pyfortran.py demo/fibo.f
echo "=============================="
python pyfortran.py demo/array.f
echo "=============================="
python pyfortran.py demo/pi.f
echo "=============================="
python pyfortran.py demo/loop.f
echo "=============================="
python pyfortran.py demo/loop2.f
echo "=============================="
python pyfortran.py demo/cont.f
echo "=============================="
python pyfortran.py demo/compgoto.f

