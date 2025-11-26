def es_gerente(request):
    if request.user.is_authenticated:
        return {'es_gerente': request.user.groups.filter(name='Gerente').exists()}
    return {'es_gerente': False}
