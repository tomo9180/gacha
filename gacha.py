import json
import os

import numpy


#聖遺物の部位
piece = ["生の花", "死の羽", "時の砂", "空の杯", "理の冠"]
#原神に存在する全てのステータスのリスト
status = [
    "HP",
    "攻撃力",
    "防御力",
    "HP(%)",
    "攻撃力(%)",
    "防御力(%)",
    "元素熟知",
    "元素チャージ効率(%)",
    "炎元素ダメージ(%)",
    "水元素ダメージ(%)",
    "氷元素ダメージ(%)",
    "雷元素ダメージ(%)",
    "風元素ダメージ(%)",
    "岩元素ダメージ(%)",
    "草元素ダメージ(%)",
    "会心率(%)",
    "会心ダメージ(%)",
    "与える治癒効果(%)",
]
#それぞれの部位に出現するメインステータス
clock_list = [3, 4, 5, 6, 7]
cup_list = [3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15]
crown_list = [3, 4, 5, 6, 15, 16, 17]
#それぞれの部位に出現するメインステータスの出現率
clock_prob = [0.2668, 0.2666, 0.2666, 0.1, 0.1]
cup_prob = [0.1925, 0.1925, 0.19, 0.25, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
crown_prob = [0.22, 0.22, 0.22, 0.04, 0.1, 0.1, 0.1]
#サブステータスに出現するステータス
sub_list = [0, 1, 2, 3, 4, 5, 6, 7, 15, 16]
sub_prob = [0.15, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.075, 0.075]
#サブステータスの出現率
sub_num = {
    0: [209.13, 239.00, 268.88, 298.75],
    1: [13.62, 15.56, 17.51, 19.45],
    2: [16.20, 18.52, 20.83, 23.15],
    3: [4.08, 4.66, 5.25, 5.83],
    4: [4.08, 4.66, 5.25, 5.83],
    5: [5.10, 5.83, 6.56, 7.29],
    6: [16.32, 18.65, 20.98, 23.31],
    7: [4.53, 5.18, 5.83, 6.48],
    15: [2.72, 3.11, 3.50, 3.89],
    16: [5.44, 6.22, 6.99, 7.77],
}


#未強化の聖遺物を生成
def create_artifact():
    level = 0
    piece_pick = numpy.random.choice(piece)
    if piece_pick == "生の花":
        main = 0
    elif piece_pick == "死の羽":
        main = 1
    elif piece_pick == "時の砂":
        main = numpy.random.choice(clock_list, 1, clock_prob)[0]
    elif piece_pick == "空の杯":
        main = numpy.random.choice(cup_list, 1, cup_prob)[0]
    else:
        main = numpy.random.choice(crown_list, 1, crown_prob)[0]

    #メインopがサブopに存在する場合
    if main in sub_list:
        s = sub_list.index(main)
        sub_list.remove(main)
        sub_prob.pop(s)
        #3op or 4opの抽選
        op = numpy.random.choice([3, 4], 1, [0.675, 0.325])
    #メインopがサブopに存在しない場合
    else:
        #3op or 4opの抽選
        op = numpy.random.choice([3, 4], 1, [0.8, 0.2])
    while True:
        #サブステータスの抽選
        sub_status = numpy.random.choice(sub_list, op, sub_prob)
        if len(sub_status) == len(set(sub_status)):
            break
    #サブステータスの数値の抽選・表示する小数点以下桁数をゲーム内表記に合わせる
    display_sub_num = []
    picked_sub_num = []
    f = 0
    for item in sub_status:
        picked_sub_num.append(numpy.random.choice(sub_num[item]))
        if "%" in status[item]:
            display_sub_num.append(str(round(picked_sub_num[f], 1)))
        else:
            display_sub_num.append(str(int(round(picked_sub_num[f], 0))))
        f = f + 1

    print(f"\nLv.{level} {piece_pick}\n{status[main]}\n")
    for i in range(len(picked_sub_num)):
        print(f"{status[sub_status[i]]} {display_sub_num[i]}")
    #jsonに保存
    sub_status = [str(x) for x in list(sub_status)]
    data = {"level":level,
            "piece":piece_pick,
            "main":int(main),
            "picked_sub_num":picked_sub_num,
            "sub_status":sub_status,
            "op":int(op[0])
            }
    with open(f"data.json", "w") as f:
        json.dump(data, f)


#聖遺物強化(4Lvずつ)
def enhance():
    with open(f"data.json", "r") as f:
        data = json.load(f)
    level = data["level"] + 4
    op = data["op"]
    piece = data["piece"]
    main = data["main"]
    picked_sub_num = data["picked_sub_num"]
    sub_status = [int(x) for x in data["sub_status"]]

    #3opの場合サブステータスを新たに抽選
    if op == 3:
        while True:
            temp = numpy.random.choice(sub_list, 1, sub_prob)[0]
            sub_status.append(int(temp))
            if len(sub_status) == len(set(sub_status)):
                picked_sub_num.append(numpy.random.choice(sub_num[sub_status[-1]]))
                op = 4
                break
            del sub_status[-1]

    #4opもしくはLv8以上の場合サブステータスをランダムに強化
    else:
        tmp = numpy.random.choice(4)
        picked_sub_num[tmp] = picked_sub_num[tmp] + numpy.random.choice(sub_num[sub_status[tmp]])

    #表示する小数点以下桁数をゲーム内表記に合わせる
    display_sub_num = []
    f = 0
    for item in sub_status:
        if "%" in status[item]:
            display_sub_num.append(str(round(picked_sub_num[f], 1)))
        else:
            display_sub_num.append(str(round(picked_sub_num[f], 0)))
        f = f + 1
    print(f"\nLv.{level} {piece}\n{status[main]}\n")
    for i in range(len(picked_sub_num)):
        print(f"{status[sub_status[i]]} {display_sub_num[i]}")
    #Lv20の場合jsonファイルを削除、Lv20未満の場合jsonファイルを上書き
    sub_status = [str(x) for x in list(sub_status)]
    if level != 20:
        data = {"level":level,
            "piece":piece,
            "main":int(main),
            "picked_sub_num":picked_sub_num,
            "sub_status":sub_status,
            "op":op
            }
        with open(f"data.json", "w") as f:
            json.dump(data, f)
    else:
        print("\n最大Lvに達しました")
        os.remove(f"data.json")
    return level


def main():
    try:
        create_artifact()
        print("\n次の聖遺物→1と入力してEnter\n強化→2と入力してEnter\n")
        while True:
            a = input(">>>")
            if a == "2":
                level = enhance()
                if level == 20:
                    print("\n次の聖遺物→1と入力してEnter")
                    continue
            else:
                create_artifact()
            print("\n次の聖遺物→1と入力してEnter\n強化→2と入力してEnter\n")
    except Exception as e:
        print(e)

main()
        