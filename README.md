# FlexOrder — Refatoração com Padrões de Projeto

## Descrição da Nova Arquitetura Orientada a Objetos

A nova arquitetura refatora o código monolítico original, separando responsabilidades em componentes especializados. 
O sistema agora segue os princípios de **baixo acoplamento** e **alta coesão**, facilitando manutenção e extensibilidade. 
Cada módulo possui uma função única, corrigindo as violações de **SRP (Single Responsibility Principle)** e **OCP (Open/Closed Principle)**.

A aplicação foi estruturada em três camadas conceituais:

1. **Camada de Estratégias (Strategy)** — define comportamentos intercambiáveis para pagamento e frete.
2. **Camada de Decoração (Decorator)** — adiciona dinamicamente descontos e taxas sem modificar a lógica central.
3. **Camada de Fachada (Facade)** — fornece uma interface simplificada para orquestrar todo o processo de checkout.

---

## Explicação Técnica dos Padrões Utilizados

### Padrão Strategy
**Problema resolvido:** O código legado possuía condicionais fixas (if/else) para definir tipos de pagamento e cálculo de frete, violando o **OCP**.  
**Solução:** As estratégias de pagamento e frete foram abstraídas em interfaces (`EstrategiaPagamento`, `EstrategiaFrete`), 
permitindo criar novas modalidades sem alterar o código existente.  
**Benefício:** Extensibilidade e substituição dinâmica dos comportamentos sem alterar o núcleo da aplicação.

### Padrão Decorator
**Problema resolvido:** Descontos e taxas estavam embutidos diretamente no cálculo do pedido, gerando alto acoplamento e violando o **SRP**.  
**Solução:** Criou-se uma hierarquia de classes decoradoras (`DescontoPix`, `TaxaEmbalagemPresente`) que envolvem um pedido base 
e adicionam comportamentos extras dinamicamente.  
**Benefício:** Reutilização e composição flexível de regras de precificação, sem modificar classes já existentes.

### Padrão Facade
**Problema resolvido:** A lógica de finalização da compra orquestrava várias etapas (estoque, nota fiscal, pagamento) de forma desorganizada.  
**Solução:** O padrão **Facade** foi aplicado por meio da classe `CheckoutFacade`, que centraliza as chamadas aos subsistemas 
(`SistemaEstoque`, `GeradorNotaFiscal`) oferecendo uma interface simples para o cliente.  
**Benefício:** Redução da complexidade visível ao cliente e maior isolamento das dependências internas.

---

## Conclusão

A refatoração corrigiu as violações de **SRP** (responsabilidades divididas) e **OCP** (extensão sem modificação), tornando o sistema mais robusto, 
testável e aderente aos princípios de design orientado a objetos.  
Cada novo comportamento pode ser adicionado criando novas classes concretas, sem tocar no código existente.
