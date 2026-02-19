import random
import re


class CompteCorrent:

    ID = 0

    def __init__(self, ID: int = None, num_compte: int = None, DNI: str = None, nom_titular: str = None, cognom_titular: str = None, saldo: float = None):
        # Generar identificadors simples
        self.ID = CompteCorrent.generarID()
        self.num_compte = CompteCorrent.generarNumCompte()

        self.DNI = DNI if DNI is not None else input("Introdueix el DNI del titular: ")
        self.nom_titular = nom_titular if nom_titular is not None else input("Introdueix el nom del titular: ")
        self.cognom_titular = cognom_titular if cognom_titular is not None else input("Introdueix el cognom del titular: ")
        self.saldo = saldo if saldo is not None else input("Introdueix el saldo inicial: ")

    @classmethod
    def generarID(cls):
        cls.ID += 1
        return cls.ID

    @classmethod
    def generarNumCompte(cls):
        return random.randint(10000000, 99999999)

    def _normalize_saldo(self):
        while True:
            try:
                if isinstance(self.saldo, (int, float)):
                    saldo_valor = float(self.saldo)
                else:
                    saldo_valor = float(str(self.saldo).replace(",", ".").strip())
                if saldo_valor < 0:
                    raise ValueError("negatiu")
                self.saldo = int(saldo_valor) if saldo_valor.is_integer() else saldo_valor
                return True
            except Exception:
                print("Saldo invàlid. Introdueix un nombre no negatiu.")
                self.saldo = input("Introdueix el saldo inicial: ")

    def verificarDades(self):
        """Verifica i, si cal, torna a demanar DNI, nom, cognom i saldo fins que siguin vàlids."""

        def textValid(s: str) -> bool:
            if not isinstance(s, str):
                return False
            s = s.strip()
            if not s:
                return False
            # Permetre només lletres i espais
            net = s.replace(" ", "")
            return net.isalpha()

        # DNI
        while True:
            dni = str(self.DNI).strip().upper()
            if re.match(r'^\d{8}[A-Z]$', dni):
                self.DNI = dni
                break
            print("Error en DNI")
            self.DNI = input("Introdueix DNI: ")

        # Nom
        while not textValid(self.nom_titular):
            print("Nom invàlid. Ha de contenir només lletres i espais i no estar buit.")
            self.nom_titular = input("Introdueix el nom del titular: ")

        # Cognom
        while not textValid(self.cognom_titular):
            print("Cognom invàlid. Ha de contenir només lletres i espais i no estar buit.")
            self.cognom_titular = input("Introdueix el cognom del titular: ")

        # Saldo
        self._normalize_saldo()
        return True

    def ingressar_diners(self, quantitat):
        """Ingressa una quantitat positiva al compte. Retorna True si ok, False si error."""
        try:
            q = float(quantitat)
            if q <= 0:
                print("La quantitat ha de ser positiva.")
                return False
        except Exception:
            print("Quantitat invàlida.")
            return False

        # Assegurar saldo normalitzat
        try:
            saldo_actual = float(self.saldo)
        except Exception:
            if not self._normalize_saldo():
                return False
            saldo_actual = float(self.saldo)

        nou = saldo_actual + q
        self.saldo = int(nou) if nou.is_integer() else nou
        print(f"Ingressats {q:.2f} €. Nou saldo: {self.saldo} €")
        return True

    def retirada_efectiu(self, quantitat):
        """Retira una quantitat si hi ha fons suficients. Retorna True si ok, False si error."""
        try:
            q = float(quantitat)
            if q <= 0:
                print("La quantitat ha de ser positiva.")
                return False
        except Exception:
            print("Quantitat invàlida.")
            return False

        try:
            saldo_actual = float(self.saldo)
        except Exception:
            if not self._normalize_saldo():
                return False
            saldo_actual = float(self.saldo)

        if q > saldo_actual:
            print("Fons insuficients.")
            return False

        nou = saldo_actual - q
        self.saldo = int(nou) if nou.is_integer() else nou
        print(f"Retirats {q:.2f} €. Nou saldo: {self.saldo} €")
        return True

    def veure_saldo(self):
        """Retorna el saldo"""
        try:
            saldo_actual = float(self.saldo)
            # Mostrar sense decimals si és enter
            if saldo_actual.is_integer():
                return f"{int(saldo_actual)} €"
            return f"{saldo_actual:.2f} €"
        except Exception:
            self._normalize_saldo()
            return self.veure_saldo()

    def veure_dades(self):
        return (f"ID: {self.ID}\nNum compte: {self.num_compte}\nDNI: {self.DNI}\n" \
                f"Nom: {self.nom_titular} {self.cognom_titular}\nSaldo: {self.veure_saldo()}")


def menu_compte(cc: CompteCorrent):
    print("\n--- Menú Compte Corrent ---")
    while True:
        print("\n1) Ingressar diners\n2) Retirada d'efectiu\n3) Veure saldo\n4) Veure dades del compte\n5) Sortir")
        opt = input("Tria una opció (1-5): ").strip()
        if opt == '1':
            q = input("Quantitat a ingressar: ")
            cc.ingressar_diners(q)
        elif opt == '2':
            q = input("Quantitat a retirar: ")
            cc.retirada_efectiu(q)
        elif opt == '3':
            print("Saldo:", cc.veure_saldo())
        elif opt == '4':
            print(cc.veure_dades())
        elif opt == '5':
            print("Fins aviat!")
            break
        else:
            print("Opció invàlida. Intenta-ho de nou.")


if __name__ == '__main__':
    compte = CompteCorrent()
    compte.verificarDades()
    menu_compte(compte)
    
