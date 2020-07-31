from flask import Flask, render_template, url_for, request, jsonify, make_response

def execute2(a,b):
    print("execute2() has been executed")
    print(type(a))
    d=0
    d= int(a) + int(2) + int(b)
    return d

def execute3(d,c):
    print("execute3() has been executed")
    print(type(d))
    e=0
    e= d + int(1) + c
    return e