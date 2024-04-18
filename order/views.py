from django.shortcuts import render
from seller.models import Food
from .models import Cart


def order_detail(request, pk):
  food = Food.objects.get(pk=pk)
  context = {
    'object' : food
  }
  return render(request, 'order\order_detail.html', context)


from django.http import JsonResponse
from django.db.models import Sum

def modify_cart(request):
  # A사용자가 카드에 담은 B 음식에 대해서 수량을 조정하는 내용
  # 응답 : 새롭게 변경된 수량(현재수량 - currentQuantity), 전체 카트 음식 수량(장바구니 - totalQuantity)
  # 어떤 사용자?
  user = request.user
  # 어떤 음식?
  food_id = request.POST['foodId']
  food = Food.objects.get(pk=food_id)
  # 카트정보
  cart, created = Cart.objects.get_or_create(food=food, user=user)
  # 수량 업데이트 : 어떤 음식(food_id)에 amount를 amountChange만큼 변경
  cart.amount += int(request.POST['amountChange'])
  if cart.amount > 0:
     cart.save()
  elif cart.amount <= 0:
      cart.amount = 0
      cart.save()

  # '내'(user)가 카트에 담은(cart) 전체 음식 개수 <-> 개별 개수(amount)
  # Question - Choice 
  # 이 문제에 대한 초이스
  # question.choice_set
  totalQuantity = user.cart_set.aggregate(totalcount=Sum('amount'))['totalcount']

  # 변경된 최종 결과를 반환(JSON)
  context = {
     'newQuantity' : cart.amount,
     'totalQuantity' : totalQuantity,   
      'message':'수량이 성공적으로 업데이트 되었습니다.',
      'success':True
  }
  return JsonResponse(context)
