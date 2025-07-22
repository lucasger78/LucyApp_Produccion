from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Cliente, Pedido, ItemPedido
from .forms import ClienteForm
import json
from decimal import Decimal, InvalidOperation
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.http import Http404
from django.template.loader import get_template
# from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
#from django.contrib.auth.decorators import login_required




# @login_required
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'pedidos/catalogo.html', {'productos': productos})

# @csrf_exempt
def guardar_carrito(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request.session['carrito'] = data['productos']
            request.session['total_carrito'] = data['total']
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# @login_required
def formulario_cliente(request):
    # Verificar carrito
    if 'carrito' not in request.session or not request.session['carrito']:
        messages.error(request, 'No hay productos en el carrito')
        return redirect('catalogo')

    total = request.session.get('total_carrito', '0.00')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                # Guardar cliente
                cliente = form.save()
                empleado = form.cleaned_data['empleado']

                # Crear pedido
                pedido = Pedido.objects.create(
                    cliente=cliente,
                    empleado=empleado,
                    total=Decimal(total),
                    seña=form.cleaned_data.get('seña', Decimal('0')),
                    completado=False
                )

                # Guardar items del carrito
                for item in request.session['carrito']:
                    producto = Producto.objects.get(id=item['id'])
                    ItemPedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item['cantidad'],
                        subtotal=Decimal(item['subtotal'])
                    )

                # Limpiar sesión y redirigir
                del request.session['carrito']
                request.session['pedido_id'] = pedido.id
                return redirect('verificar_pedido')

            except Exception as e:
                messages.error(request, f'Error al procesar: {str(e)}')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = ClienteForm()

    return render(request, 'pedidos/formulario_cliente.html', {
        'form': form,
        'total': total
    })




# def enviar_pedido(request):
    # if request.method != 'POST':
    #     return redirect('catalogo')

    # try:
    #     carrito_data = request.POST.get('carrito', '{}')
    #     carrito = json.loads(carrito_data)

    #     if not carrito:
    #         messages.error(request, 'El carrito está vacío')
    #         return redirect('formulario_cliente')

    #     # Datos del cliente
    #     nombre = request.POST.get('nombre_completo', '').strip()
    #     email = request.POST.get('email', '').strip()
    #     telefono = request.POST.get('telefono', '').strip()

    #     if not nombre or not email or not telefono:
    #         messages.error(request, 'Todos los campos son obligatorios')
    #         return redirect('formulario_cliente')

    #     try:
    #         senia = Decimal(request.POST.get('senia', 0))
    #     except:
    #         senia = Decimal(0)

    #     # Crear cliente
    #     cliente = Cliente.objects.create(
    #         nombre_completo=nombre,
    #         email=email,
    #         telefono=telefono
    #     )

    #     # Calcular total y crear items del pedido (sin imagen)
    #     total = Decimal(0)
    #     items = []

    #     for producto_id, cantidad in carrito.items():
    #         producto = get_object_or_404(Producto, id=producto_id)
    #         cantidad = int(cantidad)
    #         if cantidad <= 0:
    #             continue

    #         subtotal = producto.precio * Decimal(cantidad)
    #         total += subtotal

    #         items.append({
    #             'producto': producto,
    #             'cantidad': cantidad,
    #             'subtotal': subtotal
    #         })

    #     if not items:
    #         messages.error(request, 'No hay productos válidos en el carrito')
    #         return redirect('formulario_cliente')

    #     # Crear pedido
    #     pedido = Pedido.objects.create(
    #         cliente=cliente,
    #         total=total,
    #         senia=senia,
    #         total_final=max(total - senia, Decimal(0))
    #     )

    #     # Crear items del pedido (sin guardar imagen)
    #     for item in items:
    #         ItemPedido.objects.create(
    #             pedido=pedido,
    #             producto=item['producto'],  # Solo guarda referencia al producto
    #             cantidad=item['cantidad'],
    #             subtotal=item['subtotal']
    #         )

    #     return redirect('gracias')

    # except Exception as e:
    #     messages.error(request, f'Error al procesar el pedido: {str(e)}')
    #     return redirect('formulario_cliente')
    

    
    
# @login_required
# def resumen_pedido(request):
#     # Verificar carrito existe y no está vacío
#     carrito = request.session.get('carrito', {})
#     if not carrito:
#         messages.warning(request, "No hay productos en el carrito")
#         return redirect('catalogo')

#     if request.method == 'POST':
#         form = ClienteForm(request.POST)
#         if form.is_valid():
#             try:
#                 # 1. Guardar cliente en sesión (no en BD todavía)
#                 request.session['cliente_data'] = {
#                     'nombre_completo': form.cleaned_data['nombre_completo'],
#                     'email': form.cleaned_data['email'],
#                     'telefono': form.cleaned_data['telefono'],
#                     'senia': str(form.cleaned_data.get('senia', 0))
#                 }
                
#                 # 2. Guardar items del carrito en sesión
#                 items = []
#                 total = 0
#                 for producto_id, item in carrito.items():
#                     producto = Producto.objects.get(id=producto_id)
#                     subtotal = producto.precio * int(item['cantidad'])
#                     items.append({
#                         'producto_id': producto_id,
#                         'nombre': producto.nombre,
#                         'cantidad': item['cantidad'],
#                         'precio': str(producto.precio),
#                         'subtotal': str(subtotal)
#                     })
#                     total += subtotal
                
#                 request.session['pedido_items'] = items
#                 request.session['pedido_total'] = str(total)
#                 request.session.modified = True
                
#                 # 3. Redirigir a confirmación REAL
#                 return redirect('verificar_pedido')  # Nueva vista que crearemos
                
#             except Exception as e:
#                 messages.error(request, f"Error: {str(e)}")
#         else:
#             messages.error(request, "Corrige los errores en el formulario")
#     else:
#         form = ClienteForm()

#     # Mostrar resumen (código existente)
#     return render(request, 'pedidos/verificar_pedido.html', {
#         'form': form,
#         'items': [...]  # Tus items calculados
#     })
    
# # @login_required    
# def confirmar_pedido(request):
#     # Verificar si hay pedido pendiente de confirmar
#     pedido_id = request.session.get('pedido_a_confirmar')
#     if not pedido_id:
#         messages.error(request, "No hay pedido pendiente de confirmar")
#         return redirect('catalogo')

#     try:
#         pedido = Pedido.objects.get(id=pedido_id)
        
#         if request.method == 'POST':
#             # Marcar como COMPLETO y limpiar sesión
#             pedido.completado = True
#             pedido.save()
            
#             # Limpiar carrito y datos temporales
#             if 'carrito' in request.session:
#                 del request.session['carrito']
#             if 'pedido_a_confirmar' in request.session:
#                 del request.session['pedido_a_confirmar']
            
#             return redirect('gracias', pedido_id=pedido.id)
        
#         # Mostrar página de confirmación
#         return render(request, 'pedidos/verificar_pedido.html', {
#             'pedido': pedido,
#             'items': pedido.items.all()
#         })
        
#     except Pedido.DoesNotExist:
#         messages.error(request, "El pedido no existe")
#         return redirect('catalogo')
    
# @login_required
def verificar_pedido(request):
    if 'pedido_id' not in request.session:
        messages.error(request, 'No hay pedido para verificar')
        return redirect('catalogo')

    try:
        pedido = Pedido.objects.get(id=request.session['pedido_id'])
        items = ItemPedido.objects.filter(pedido=pedido)

        if request.method == 'POST':
            pedido.completado = False
            pedido.save()
            del request.session['pedido_id']
            return redirect('gracias')

        return render(request, 'pedidos/verificar_pedido.html', {
            'pedido': pedido,
            'items': items
        })

    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado')
        return redirect('catalogo')
    
# @login_required   
def generar_pdf_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = ItemPedido.objects.filter(pedido=pedido)
    
    template_path = 'pedidos/verificar_pedido_pdf.html'
    context = {'pedido': pedido, 'items': items}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedido_{pedido_id}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response
    
# @login_required
def lista_productos_api(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio')
    return JsonResponse(list(productos), safe=False)


def gracias(request):
    return render(request, 'pedidos/gracias.html')