# # from random import randint
# #
# #
# # random_card_num = [randint(1,9999) for card_num in range(4)]
# # random_card_num_for_print = ','.join(random_card_num)
# #
# #
# # print(random_card_num_for_print)
# #
# # from random import randint
# #
# # random_card_num = [str(randint(1000, 9999)) for _ in range(4)]
# # random_card_num_for_print = ' '.join(random_card_num)
# #
# # print(random_card_num_for_print)
#
# # card = "CREDITCARDNUMBER"
# # print ("*" * (len(card) - 4) + card[-4:])
#
# def mask_phone_number(number: str) -> str:
#     return number[:3] + '****' + number[7:]
#
# masked_number = mask_phone_number('01012345678')
# print(masked_number)  # 출력: '010****5678'
# #
number1 = '010'
number2 = '0102863'
number3 = '01028639'
list_ = [number1, number2, number3]
for i in list_:
    if len(i) <= 3:
        print(i)
    elif 3 < len(i) <8:
        print(f'{i[:3]}-{(len(i)-3)*"*"}')
    else:
        print(i[:3] + '-****' + i[7:])


    # print(f'{number[:3]}-{(len(number)-3)*"*"}')


