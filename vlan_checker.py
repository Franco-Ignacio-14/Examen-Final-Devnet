vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN corresponde a un rango NORMAL")
elif 1006 <= vlan <= 4094:
    print("La VLAN corresponde a un rango EXTENDIDO")
else:
    print("El número ingresado NO corresponde a una VLAN válida")
