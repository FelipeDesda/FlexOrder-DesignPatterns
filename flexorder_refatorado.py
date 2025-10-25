from abc import ABC, abstractmethod
from dataclasses import dataclass

class EstrategiaPagamento(ABC):
    @abstractmethod
    def pagar(self, valor: float) -> None:
        pass

class PagamentoPix(EstrategiaPagamento):
    def pagar(self, valor: float) -> None:
        print(f"[Pagamento] Pagamento via PIX realizado: R${valor:.2f}")

class PagamentoCredito(EstrategiaPagamento):
    def pagar(self, valor: float) -> None:
        print(f"[Pagamento] Pagamento via Cartão de Crédito realizado: R${valor:.2f}")

class EstrategiaFrete(ABC):
    @abstractmethod
    def calcular(self, distancia_km: float) -> float:
        pass

class FreteNormal(EstrategiaFrete):
    def calcular(self, distancia_km: float) -> float:
        base = 10.0
        por_km = 0.5
        return base + por_km * distancia_km

class FreteExpresso(EstrategiaFrete):
    def calcular(self, distancia_km: float) -> float:
        base = 20.0
        por_km = 1.2
        return base + por_km * distancia_km

class PedidoBase(ABC):
    @abstractmethod
    def calcular(self) -> float:
        pass

class PedidoConcreto(PedidoBase):
    def __init__(self, valor: float):
        self._valor = valor

    def calcular(self) -> float:
        return self._valor

class DescontoPix(PedidoBase):
    def __init__(self, pedido: PedidoBase, percentual: float = 0.05):
        self._pedido = pedido
        self._percentual = percentual

    def calcular(self) -> float:
        base = self._pedido.calcular()
        desconto = base * self._percentual
        return base - desconto

class TaxaEmbalagemPresente(PedidoBase):
    def __init__(self, pedido: PedidoBase, taxa: float = 10.0):
        self._pedido = pedido
        self._taxa = taxa

    def calcular(self) -> float:
        return self._pedido.calcular() + self._taxa

class SistemaEstoque:
    def atualizar(self):
        print("[Estoque] Estoque atualizado: decrementando quantidades.")

class GeradorNotaFiscal:
    def gerar(self, pedido_valor=None):
        print(f"[NotaFiscal] Nota fiscal gerada. Valor: R${pedido_valor:.2f}" if pedido_valor is not None else "[NotaFiscal] Nota fiscal gerada.")

class CheckoutFacade:
    def __init__(self, sistema_estoque, gerador_nota_fiscal):
        self.sistema_estoque = sistema_estoque
        self.gerador_nota_fiscal = gerador_nota_fiscal

    def concluir_transacao(self, pedido, pedido_decorado):
        self.sistema_estoque.atualizar()
        try:
            valor_final = pedido_decorado.calcular()
        except Exception:
            valor_final = pedido.valor_base
        self.gerador_nota_fiscal.gerar(pedido_valor=valor_final)
        print("[Checkout] Transação concluída com sucesso.")

@dataclass
class Pedido:
    valor_base: float
    estrategia_pagamento: object
    estrategia_frete: object

    def calcular_total(self, distancia_km: float) -> float:
        frete_valor = self.estrategia_frete.calcular(distancia_km)
        return self.valor_base + frete_valor

    def processar_pagamento(self, distancia_km: float) -> None:
        total = self.calcular_total(distancia_km)
        self.estrategia_pagamento.pagar(total)

if __name__ == '__main__':
    pagamento = PagamentoPix()
    frete = FreteExpresso()
    pedido = Pedido(valor_base=200.0, estrategia_pagamento=pagamento, estrategia_frete=frete)

    distancia_km = 12
    total_com_frete = pedido.calcular_total(distancia_km)
    print(f"Total (base + frete): R${total_com_frete:.2f}")

    pedido_base = PedidoConcreto(total_com_frete)
    pedido_decorado = TaxaEmbalagemPresente(DescontoPix(pedido_base))
    total_final = pedido_decorado.calcular()
    print(f"Total final (desconto + taxa): R${total_final:.2f}")

    pedido.processar_pagamento(distancia_km)

    estoque = SistemaEstoque()
    nota = GeradorNotaFiscal()
    checkout = CheckoutFacade(estoque, nota)
    checkout.concluir_transacao(pedido, pedido_decorado)
