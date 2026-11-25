<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Gerenciador de pilotagem do TAILSCALE com firewall integrado para o FUNNEL**

O OMEGA-TAIL é a ferramenta da suíte OMEGA que pilota o **Tailscale** em uma máquina e a **protege** quando ela
publica um serviço na Internet pelo **Tailscale Funnel**.

> Desenvolvido por [kraynux](https://github.com/kraynux) para [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Página oficial](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/pt-BR/) · [Capturas de tela](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interface, documentação, exportações e páginas para visitantes disponíveis em **17 idiomas** — veja [Idiomas da interface](#idiomas-da-interface).  
**Idiomas:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

O **OMEGA-TAIL** é um aplicativo TUI (Terminal User Interface) em Python construído com
[Textual](https://textual.textualize.io/). Ele permite gerenciar e configurar o **Tailscale** em modo avançado a partir
de uma interface, sem decorar um único comando. Ele também acrescenta proteções (firewall, confinamento,
sobrevivência…) para o modo **Funnel**, que abre um serviço da máquina para toda a Internet.

Cada ação que altera a máquina mostra antes o seu comando. A senha do sudo é digitada no terminal, ação por ação,
e nada é executado em segundo plano sem você.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/pt-BR/omega-tail/F.png" width="32%" />
</p>

O projeto é concebido segundo os princípios da **Clean Architecture**, com `app/` como raiz de composição: o
domínio de negócio, a orquestração, a infraestrutura e a interface são separados.

## Sumário

- [Apresentação](#apresentação)
- [Entendendo o Tailscale e o Funnel](#entendendo-o-tailscale-e-o-funnel)
- [Funcionalidades](#funcionalidades)
- [As proteções em detalhe](#as-proteções-em-detalhe)
- [Medições](#medições)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Temas e terminais](#temas-e-terminais)
- [Arquivos, serviços e compatibilidade](#arquivos-serviços-e-compatibilidade)
- [Segurança](#segurança)
- [Testes e qualidade](#testes-e-qualidade)
- [Estado do projeto](#estado-do-projeto)
- [Desinstalação](#desinstalação)
- [Licença](#licença)

---

## Apresentação

### Por que o omega-tail

O Tailscale Funnel publica um serviço da máquina na Internet sem abrir nenhuma porta no roteador: os visitantes
passam pelos retransmissores do Tailscale. É simples e seguro do lado da rede, mas resta uma fraqueza.

- **O custo da criptografia.** No modo Funnel padrão, é o serviço `tailscaled` da máquina que faz o handshake TLS
  de cada visitante. Medido em uma máquina pequena, isso representa cerca de **80 % do custo de uma conexão**.
  Algumas centenas de novas conexões por segundo bastam para saturar o processador: um único computador comum,
  com um simples script, pode derrubar o site e a máquina.
- **Visitantes invisíveis.** Os firewalls habituais (nftables, ufw, fail2ban) não veem esses visitantes: eles
  chegam criptografados, pelo túnel do Tailscale, com o endereço de um retransmissor.
- **Configurações dispersas.** As configurações do Tailscale (operador, nó de saída, rotas, SSH, escudo…) são
  numerosas, divididas entre comandos e console web, e algumas podem derrubar a sessão em curso.

### Objetivos

- Pilotar o Tailscale inteiramente a partir de uma interface, com uma frase de explicação para cada configuração.
- Recusar as conexões abusivas **antes** de qualquer criptografia, vendo o endereço real de cada visitante.
- Manter a máquina de pé sob ataque: a administração e os outros serviços continuam acessíveis.
- Nunca impor nada: propor, mostrar o comando, perguntar e poder voltar atrás.
- Funcionar em qualquer distribuição Linux, com systemd, OpenRC ou runit.

### O que o omega-tail faz

- Exibe o estado do Tailscale, da máquina e do que está publicado, com alertas que levam à tela que corrige o
  problema.
- Inicia, para e reinicia o `tailscaled`, com uma proteção caso a sua sessão passe pelo Tailscale.
- Gerencia a conexão, as contas e todas as configurações de `tailscale set`, verificadas antes de serem aplicadas.
- Publica, remove, suspende e testa os serviços do Serve e do Funnel, com backups e restauração.
- Mostra os dispositivos do tailnet, o caminho de cada um (direto ou retransmitido), um diagnóstico de rede e os logs.
- Coloca um **portão** HAProxy entre o Funnel e o seu site: regras por endereço, por prefixo, orçamento global,
  listas de confiança e negra, agrupamentos por impressão digital JA4, rede de origem (AS) e país, modo ataque
  automático.
- Confina o `tailscaled`, corta o Funnel por um tempo ou totalmente, e pode fazer isso sozinho graças a uma
  vigilância automática.
- Protege a porta WireGuard do `tailscaled` com uma tabela nftables (escudo).
- Produz um relatório da máquina e dos ataques dos últimos 7 dias, em TXT, HTML ou JSON.

### O que o projeto não faz

- Ele não substitui o Tailscale: ele o pilota.
- Ele não protege contra um ataque volumétrico que satura a própria linha de Internet (o roteador, o link).
- Ele não gerencia o console de administração web do Tailscale (política de acesso, aprovação dos nós de saída,
  ativação do Funnel para o tailnet).
- Ele não protege um serviço publicado de outra forma que não pelo Funnel: para essas portas, existe o omega-fire.
- Ele nunca é executado como root e não executa nada em segundo plano sem o seu consentimento.
- Ele não funciona no Windows nem no macOS.

[↑ Sumário](#sumário)

---

## Entendendo o Tailscale e o Funnel

O omega-tail pressupõe algumas noções de Tailscale. Esta parte as reúne, sem pressupor mais nada.

### O vocabulário

| Termo | O que é |
|---|---|
| **Tailnet** | A sua rede privada Tailscale: todas as máquinas conectadas à mesma conta (ou à mesma organização). Cada máquina recebe nela um endereço em `100.x.y.z` (faixa 100.64.0.0/10) e um endereço IPv6 em `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | O serviço (daemon) que roda na máquina: ele mantém o túnel criptografado WireGuard, a pilha de rede do Tailscale e, para o Serve e o Funnel, a retransmissão para os seus serviços. |
| **`tailscale`** | O comando que pilota o `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). O omega-tail o usa por você. |
| **WireGuard** | O protocolo de túnel criptografado usado entre as máquinas. Para isso, o `tailscaled` escuta em uma porta UDP (41641 por padrão), muitas vezes aberta pelo roteador (UPnP). |
| **Retransmissor DERP (DERP relay)** | Servidores do Tailscale que retransmitem o tráfego quando duas máquinas não conseguem se alcançar diretamente (NAT difícil). O caminho « direto » é mais rápido. |
| **MagicDNS** | Os nomes das máquinas do tailnet, na forma `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Publicar um serviço local (um site, uma API…) **somente para o tailnet**, em HTTPS com um certificado `*.ts.net` válido. |
| **Funnel** | Publicar um serviço local **para toda a Internet**, no endereço `https://machine.nom-du-tailnet.ts.net`. Somente as portas 443, 8443 e 10000 podem ser abertas. |
| **Retransmissor Funnel (Funnel relay)** | Os servidores do Tailscale que recebem os visitantes da Internet e os fazem entrar no seu tailnet (eles aparecem como « funnel-ingress-node »). |
| **Operador (operator)** | Uma conta Linux autorizada a configurar o Tailscale sem sudo (`tailscale set --operator=…`). O omega-tail propõe isso uma vez, via sudo. |
| **Nó de saída (exit node)** | Uma máquina do tailnet pela qual outra faz passar todo o seu tráfego de Internet (como uma VPN). Ele precisa ser aprovado no console do Tailscale. |
| **Sub-rede anunciada (subnet router)** | Uma rede local (por exemplo `192.168.1.0/24`) que uma máquina torna acessível ao resto do tailnet. |
| **Escudo (shields up)** | Configuração do Tailscale que recusa todas as conexões de entrada vindas do tailnet. |
| **SSH Tailscale** | Um servidor SSH fornecido pelo Tailscale, autorizado pela política do tailnet. |
| **Cabeçalho PROXY v2** | Um cabeçalho curto adicionado no início de uma conexão para transmitir o endereço real do visitante a quem a recebe. |
| **Impressão digital JA4 (JA4 fingerprint)** | Uma assinatura da forma como um software abre uma conexão TLS: um navegador e uma ferramenta de ataque não têm a mesma. |
| **AS (sistema autônomo)** | A rede de origem de um endereço: provedor de acesso, hospedagem, nuvem. |

### O caminho de um visitante

**Funnel padrão, sem o omega-tail.** O `tailscaled` faz tudo: ele descriptografa o túnel WireGuard, faz o handshake
TLS do visitante e depois retransmite a requisição em HTTP para o seu site. Nenhum firewall da máquina vê o
visitante, e cada nova conexão custa caro ao `tailscaled`.

```text
Visitante ──HTTPS──▶ Retransmissor Funnel ──WireGuard──▶ tailscaled (TLS + retransmissão HTTP) ──HTTP──▶ seu site
                     (Tailscale)                         └── todo o custo está aqui
```

**Funnel com o portão do omega-tail.** O Funnel passa para o modo TCP: o `tailscaled` não faz mais TLS, ele
transmite o fluxo ainda criptografado ao portão, precedido do endereço real do visitante (cabeçalho PROXY v2). O
portão decide **antes** de qualquer criptografia: uma conexão recusada não custa quase nada, e somente as conexões
admitidas são descriptografadas, pelo OpenSSL, mais rápido que o TLS do `tailscaled`.

```text
Visitante ──HTTPS──▶ Retransmissor Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                              │
                                                              ▼
                                               Portão omega-tail (HAProxy, 127.0.0.1)
                                               ├── recusa antes do TLS: lista negra, taxa, orçamento, nome visado, agrupamentos
                                               └── admitido: TLS (certificado *.ts.net) ──HTTP──▶ seu site
```

O portão escuta somente na interface de loopback da máquina e roda sob a sua conta. As máquinas do seu tailnet
são sempre admitidas, antes de qualquer regra: somente os visitantes do Funnel são filtrados.

### O que o Tailscale deve permitir (console de administração)

Estas configurações são feitas uma vez, no console web do Tailscale; o omega-tail não as altera.

- **MagicDNS** e os **certificados HTTPS** ativados para o tailnet (necessários ao Serve, ao Funnel e ao
  certificado do portão).
- **Funnel autorizado** para a máquina na política de acesso do tailnet (atributo `funnel`).
- Para um nó de saída ou sub-redes anunciadas: a sua **aprovação** no console.

[↑ Sumário](#sumário)

---

## Funcionalidades

O menu principal tem duas colunas de seis: **TAILSCALE** para pilotar, **PROTEÇÃO** para defender.

### TAILSCALE

#### 1. Painel

- **Tailscale**: serviço, estado da conexão, versão em execução e instalada, nome da máquina, endereços, conta,
  dispositivos online, expiração da chave, operador, nó de saída oferecido e usado, sub-redes anunciadas.
- **Máquina**: CPU da máquina inteira, carga por núcleo, temperatura, memória, CPU e memória do `tailscaled`,
  confinamento e, em seguida, o estado das proteções (Funnel, firewall e modo ataque, lista negra, vigilância,
  escudo).
- **Publicação**: cada porta publicada, para a Internet (Funnel) ou para o tailnet (Serve), seu modo e seu destino.
- **Alertas**, do mais grave ao menos grave, com « Corrigir », que abre a tela correspondente. Por exemplo:
  serviço parado, atualização instalada mas não aplicada, chave expirando, Funnel publicado sem proteção,
  temperatura elevada, `tailscaled` consumindo demais ou não confinado, lista negra que cresce.
- Valores em verde, laranja ou vermelho conforme limites (CPU, carga, temperatura, memória, `tailscaled`).

#### 2. Serviço tailscaled

- Estado visto pelo sistema de init, versão em execução e instalada, comando de inicialização, arquivos de
  complemento (drop-in), confinamento.
- **Iniciar**, **Parar**, **Reiniciar** (por exemplo para aplicar uma atualização já instalada).
- **Proteção**: se a sua sessão passa pelo Tailscale (SSH pelo tailnet), Parar pede uma segunda confirmação,
  pois você não conseguiria mais reiniciá-lo.
- **Corrigir a inicialização**: detecta um arquivo de complemento que executa `tailscale up` na inicialização e
  corre o risco de tirar a máquina do tailnet na primeira mudança de configuração; a correção é mostrada e o
  original é guardado.

#### 3. Conexão e configurações

- **Conectar**, **Desconectar**, **Adicionar uma conta**, **Trocar de conta**, **Desconexão definitiva**
  (nome da máquina a digitar).
- **Todas as configurações de `tailscale set`**, cada uma com sua frase de explicação: nome e apelido da máquina,
  rotas, DNS do tailnet, escudo, filtragem com estado, modo netfilter, nó de saída, acesso à rede local,
  oferecer a máquina como nó de saída, sub-redes anunciadas, SSH Tailscale, interface web, atualizações,
  retransmissão entre pares, operador.
- Durante a digitação, um quadro mostra **antes → depois** e o comando; após a aplicação, cada valor relido é
  marcado com ✔ (aplicado) ou ✖ (não aplicado).
- Um aviso alerta quando uma mudança pode derrubar uma sessão que passa pelo Tailscale.
- **Encaminhamento IP**: ativado com um botão quando a máquina serve de nó de saída ou anuncia sub-redes.

#### 4. Publicação

- Tudo o que a máquina publica: porta, público (Funnel) ou tailnet (Serve), modo, caminho, destino, proteção.
- **Publicar** um serviço local em HTTPS, HTTP, TCP ou TLS terminado; **Remover**; **Suspender o Funnel** e
  **Restabelecer o Funnel** (de forma idêntica).
- **Teste de ponta a ponta**: uma conexão real, como um visitante (resposta, tempo, certificado, versão do TLS).
- **Backups**: o estado anterior a cada mudança (os 50 mais recentes), restauráveis.
- Cada mudança é verificada; em caso de divergência, a publicação é reconstruída, senão o estado anterior é
  restaurado.

#### 5. Rede e dispositivos

- **Dispositivos** do tailnet: sistema, online ou não, caminho (direto ou por retransmissor), última vez visto,
  endereço, tráfego trocado; os retransmissores Funnel do Tailscale ficam ocultos por padrão.
- **Ping Tailscale** (caminho e latência), **Quem é?** (a quem pertence um endereço do tailnet).
- **Diagnóstico de rede**: UDP, IPv4 / IPv6, tipo de NAT, abertura de porta pelo roteador (UPnP, NAT-PMP, PCP),
  retransmissor mais próximo e latências.
- **DNS**, **bloqueio do tailnet** (tailnet lock) e **contadores internos** do Tailscale.
- Somente leitura: nada nesta tela altera uma configuração.

#### 6. Logs

- O log do `tailscaled` (journalctl, ou os arquivos do serviço fora do systemd) e o do portão, filtráveis e
  exportáveis.
- Cada informação tem sua cor, tirada do tema: data, processo, categoria da mensagem (controle, rede, DNS, motor
  WireGuard), endereços em negrito, erros em vermelho, avisos em laranja; para o portão, motivo da recusa,
  agrupamento, AS e país.

### PROTEÇÃO

#### 7. Firewall do Funnel

- **Instalar o HAProxy** pelo gerenciador de pacotes da distribuição (pacman, apt, dnf, zypper, apk, xbps,
  emerge).
- **Ativar a proteção**: certificado `*.ts.net`, listas, configuração verificada, serviço do portão, troca do
  Funnel e depois teste a partir da Internet; em caso de falha, a publicação original é restaurada imediatamente.
- **Desativar a proteção**: o Funnel volta exatamente ao que era antes, verificado.
- **Regras** aplicadas a quente, modo **observação** para ajustar os limites sem risco, **agrupamentos** (veja
  [As proteções em detalhe](#as-proteções-em-detalhe)).
- **Atualizar a base** AS / país (DB-IP Lite), em um processo separado.

#### 8. Sobrevivência

- **Confinamento do `tailscaled`**: teto de CPU, peso e prioridade, opção de prioridade ao acesso SSH.
- **Disjuntor do Funnel**: limites de CPU e de temperatura, corte de 10 minutos (religamento automático) ou total.
- **Vigilância automática**: a mesma coisa sem ninguém diante da tela.
- **Escudo da porta WireGuard**: botão para a sua tela (observação, ativo, aplicar, reaplicar, remover, delegar).

#### 9. Ataques e decisões

- Contadores do portão (recebidas, recusadas antes da criptografia, admitidas, em curso) e os endereços mais
  ativos, relidos a cada 2 segundos, com país, AS e estado de cada endereço.
- **Bloquear**, **Lista negra**, **Desbloquear**, **Confiança**: aplicado na hora, sem reiniciar o portão; a
  notificação diz em uma linha a ação e o lugar do endereço.
- Visões **Impressões digitais**, **AS** e **Países**; estado do modo ataque e conexões recusadas pelos
  agrupamentos.
- **Gerenciamento da lista negra**: lista completa com data de inclusão e origem, inclusão, exclusão, importação de
  um arquivo TXT (duplicatas, redes já cobertas e endereços do tailnet descartados), limpezas com prévia (por
  antiguidade, os N mais antigos, um intervalo de linhas, uma origem, tudo), exportações TXT (reimportável), HTML e
  JSON. Teto de 50 000 entradas.

#### 10. Relatório

- Tudo o que o omega-tail sabe sobre a máquina, em fatos: Tailscale, publicação, máquina, firewall, sobrevivência,
  alertas e os **ataques dos últimos 7 dias** lidos no log do portão.
- **Privacidade**: por padrão, sem a conta Tailscale nem os nomes e endereços dos dispositivos do tailnet, para
  poder enviá-lo a alguém.
- Exportações **TXT**, **HTML** (tema à escolha) e **JSON**; **Ver as exportações** abre a pasta no navegador.

#### 11. Configurações

- Idioma da interface e das exportações, tema da interface e das exportações, pastas das exportações e das
  capturas de tela, e a sua limpeza.

#### 12. Ajuda

- Uma seção por tela, os atalhos, a linha de comando e **Contato e suporte**.

[↑ Sumário](#sumário)

---

## As proteções em detalhe

Cada proteção responde a uma ameaça precisa; nenhuma é imposta.

| Proteção | Contra o quê | Onde |
|---|---|---|
| Portão (regras) | Rajadas a partir de um ou de alguns endereços, conexões que não visam o site | Firewall do Funnel |
| Agrupamentos | Ataques com endereços dispersos (milhares de endereços, uma conexão cada) | Firewall do Funnel |
| Lista negra | Endereços e redes conhecidos por atacar, mantidos por longo prazo | Ataques e decisões |
| Confinamento | `tailscaled` que tomaria a máquina inteira sob ataque | Sobrevivência |
| Disjuntor | Máquina saturada apesar de tudo: cortar o Funnel por um tempo | Sobrevivência |
| Vigilância automática | A mesma coisa, sem ninguém diante da tela | Sobrevivência |
| Escudo WireGuard | Enxurrada de pacotes UDP na porta do `tailscaled`, com o Funnel aberto ou não | Sobrevivência |

### O portão (Firewall do Funnel)

As regras se aplicam nesta ordem, todas antes da criptografia:

1. **Máquinas do tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): sempre admitidas.
2. **Lista de confiança**: nunca limitada. **Lista negra**: recusada até a sua remoção.
3. **Taxa por endereço** (40 conexões / 10 s por padrão): acima disso, o endereço é bloqueado pela duração
   escolhida (60 min por padrão).
4. **Taxa por prefixo** /24 em IPv4, /64 em IPv6.
5. **Orçamento global** de conexões admitidas por segundo: o processador nunca fica sobrecarregado.
6. **Nome visado**: uma conexão que não visa o nome da máquina é recusada.

O certificado `*.ts.net` do portão é solicitado ao Tailscale, verificado todos os dias e renovado a quente 30 dias
antes do vencimento. O modo **observação** conta tudo sem recusar nada.

### Os agrupamentos (impressões digitais, AS, países)

Contra um ataque com endereços dispersos, as regras por endereço veem cada endereço uma única vez. Por isso o
portão também classifica cada cliente por sua **impressão digital JA4**, seu **AS** e seu **país**, e conta a taxa
de cada grupo.

- **Modo ataque automático**: acima de 80 conexões de entrada por segundo (ajustável), o portão passa sozinho para
  o modo ataque, e sai dele após 5 minutos de calma.
- Somente no modo ataque: uma impressão digital desconhecida que dispara, um AS de hospedagem ou de nuvem (lista
  editável) ou um país da sua lista (vazia por padrão) que ultrapassa a sua taxa é recusado.
- Os **navegadores comuns** (Chrome, Edge, Firefox) nunca são afetados por essas regras; os **clientes conhecidos**
  (admitidos nas últimas 24 h) passam antes do orçamento global.
- **Aprendizado**: durante 7 dias, o portão aprende as impressões digitais habituais do seu site (nunca durante
  um ataque); os agrupamentos ficam em observação até lá.
- Fora de ataque, uma conexão em cada dez é classificada; em ataque, todas.
- A base AS / país é a **DB-IP Lite**, baixada e atualizada uma vez por mês.

### A sobrevivência

- **Confinamento**: um arquivo de complemento separado impõe um teto ao `tailscaled` (por exemplo um núcleo
  inteiro em uma máquina com 4 threads) e reduz a sua prioridade. A sua própria configuração nunca é modificada.
- **Disjuntor**: quando o `tailscaled` fica acima do limite de CPU (80 % de um núcleo durante 60 s por padrão) ou
  a temperatura atinge 85 °C, o omega-tail propõe cortar o Funnel por 10 minutos (religamento automático, de forma
  idêntica, mesmo com o omega-tail fechado), cortá-lo totalmente ou esperar. O tailnet nunca é cortado.
- **Vigilância automática** (desativada por padrão): um serviço sob a sua conta corta o Funnel sozinho após três
  ultrapassagens, 15 minutos na primeira vez, 30 na segunda e depois uma hora, e o religa sozinho.

### O escudo da porta WireGuard

O `tailscaled` gasta cerca de um núcleo de processador para cada 100 000 pacotes por segundo recebidos na sua porta
UDP, mesmo inválidos. O escudo é uma tabela nftables colocada à frente dele, nas placas de rede:

- os **pares conhecidos** (aqueles para quem o `tailscaled` envia) nunca são limitados;
- os handshakes são limitados a 20 por segundo e por origem;
- as outras origens têm um orçamento (500 pacotes por segundo cada uma, 5 000 no total);
- os pacotes que não são WireGuard são recusados.

Ele é aplicado primeiro em **observação** e depois em **ativo**. Se estiver conectado pelo omega-connect, o
**omega-fire** (3.7.0 ou mais recente) pode aplicá-lo e gerenciá-lo no lugar do omega-tail: é a mesma tabela, que
muda de mãos sem ser tocada.

[↑ Sumário](#sumário)

---

## Medições

As escolhas do omega-tail vêm de medições, em máquinas da mesma geração daquelas que ele protege (processadores
de 2010 a 2016, a maioria sem aceleração AES).

| Medição | Resultado |
|---|---|
| Parcela do TLS no custo de uma conexão Funnel padrão | cerca de 80 % |
| Custo de uma conexão **recusada** pelo portão, comparado ao Funnel padrão | **4,6 vezes menor** |
| Custo de uma conexão **admitida** pelo portão, comparado ao Funnel padrão | **2 vezes menor** |
| Vazão com o portão, conexões mantidas abertas (comparado a um TLS em Go como o do `tailscaled`) | **+15 %** de requisições, −20 % de CPU |
| Escudo WireGuard: enxurrada que ocupava um núcleo inteiro do `tailscaled` | **1 %** de um núcleo |
| Memória dos serviços (portão, vigilância, escudo) | cerca de 67 MB |

Portanto, o portão não degrada a vazão de um site: nessas máquinas, é a própria criptografia que limita, com ou sem
o omega-tail, e em produção o Funnel passa de qualquer forma pelos retransmissores do Tailscale e pelo roteador.

[↑ Sumário](#sumário)

---

## Arquitetura

```text
src/omega_tail/
├── app/              Raiz de composição: monta as camadas, ponto de entrada (interface, linha de comando)
├── core/             Constantes compartilhadas
├── domain/           Lógica de negócio pura: regras do portão, alertas, disjuntor, vigilância, lista negra…
├── application/      Casos de uso: publicação, firewall, sobrevivência, relatório, configurações
├── ports/            Contratos (Protocol) esperados pela aplicação
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, logs, exportações, scripts Lua
├── interfaces/       tui/ (Textual), cli/ (linha de comando), shared/ (ajuda, relatório, apresentação)
└── shared/           Idiomas (gettext)
```

### Princípios de design

- `domain/` não contém nem leitura nem escrita: tudo ali pode ser testado sem máquina.
- `application/` orquestra os casos de uso por meio do domínio e das portas (ports); a interface e a linha de
  comando chamam os mesmos casos de uso.
- Somente `infrastructure.commands` e `infrastructure.privileged` executam comandos; a interface nunca os executa
  diretamente. Essas regras são verificadas automaticamente (import-linter).
- A interface se apoia na [omega-lib](https://github.com/kraynux), a biblioteca compartilhada por toda a suíte
  OMEGA (temas, detecção do terminal, idiomas, contato e suporte, escudo WireGuard). Ela não é publicada no
  PyPI: vem embutida no arquivo (`vendor/omega-lib/`).
- Toda chamada lenta (Tailscale, HAProxy, disco, rede) roda em segundo plano: a interface nunca congela.

[↑ Sumário](#sumário)

---

## Pré-requisitos

### Sistema

- Linux, qualquer distribuição (testado no Arch Linux e derivadas).
- Python 3.10 ou superior, com o módulo `venv`.
- Um sistema de init: **systemd**, **OpenRC** ou **runit**.
- `sudo` para as ações que alteram a máquina (pedido ação por ação, nunca na inicialização).
- Um terminal de pelo menos 80×24 (veja [Temas e terminais](#temas-e-terminais)).

### Tailscale

- **Tailscale** instalado e conectado (cliente `tailscale` e serviço `tailscaled`); testado com a versão 1.104.
- Para o Funnel: MagicDNS, certificados HTTPS e Funnel autorizados no console do Tailscale (veja
  [O que o Tailscale deve permitir](#o-que-o-tailscale-deve-permitir-console-de-administração)).

### Dependências Python

Instaladas pelo `install.sh` em um ambiente virtual:

- `textual`: a interface.
- `omega-lib`: biblioteca compartilhada da suíte OMEGA, embutida no arquivo.

### Componentes obrigatórios e opcionais

O omega-tail detecta o que está presente e só ativa o que pode ser usado.

| Componente | Função | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Tudo o que o omega-tail pilota | **Obrigatório** |
| Python 3.10+, `textual`, `omega-lib` | O aplicativo | **Obrigatório** |
| systemd, OpenRC ou runit | Serviços do portão, da vigilância, do escudo | **Obrigatório** (um dos três) |
| HAProxy 3.x | O portão do Firewall do Funnel | Opcional (instalável a partir do omega-tail) |
| HAProxy com Lua | Os agrupamentos (impressões digitais, AS, países) | Opcional (caso das distribuições comuns) |
| nftables (kernel com `nft_limit`) | O escudo da porta WireGuard | Opcional |
| Leitura do log do sistema (grupo `systemd-journal`, `adm` ou `wheel`) | Logs, relatório dos ataques | Recomendado |
| Navegador e ambiente gráfico | « Ver as exportações » no navegador (senão, leitura no omega-tail) | Opcional |
| omega-connect | Registro, sincronização, atualizações da suíte | Opcional |
| omega-fire 3.7.0+ | Gerenciamento do escudo WireGuard a partir do omega-fire | Opcional |

[↑ Sumário](#sumário)

---

## Instalação

O arquivo oficial é fornecido no formato `.tar.gz`. Verifique a sua integridade antes da instalação, com o arquivo
`sha.txt` publicado ao lado:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Estes três métodos servem para uma primeira instalação.** Se `~/omega-tail` já existir, use a
> seção [Atualização](#atualização). Nunca execute estes comandos de dentro de uma pasta
> `omega-tail` existente: o `tar` criaria um `omega-tail/omega-tail/` aninhado.

Nenhuma etapa da instalação pede direitos de root: o omega-tail é executado como usuário normal.

### Método 1 — script de instalação

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Você parece já estar em uma pasta omega-tail — veja a seção Atualização do README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Já extraído aqui, etapa ignorada." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail já existe, movimentação ignorada." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

O script cria o ambiente virtual, instala as dependências (a omega-lib embutida primeiro), torna os lançadores
executáveis, grava o token de instalação lido pelo omega-connect e propõe o alias `omega-tail`. Ele pode ser
executado de novo sem risco.

### Método 2 — instalação completa resiliente

Este comando pode ser executado de novo: ele ignora as etapas já realizadas.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Você parece já estar em uma pasta omega-tail — veja a seção Atualização do README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail já existe, extração ignorada." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv já existe, etapa ignorada." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail instalado. Execute ./omega-tail.sh."
```

### Método 3 — instalação detalhada

```bash
# 0. Verificar que não se está executando de dentro de um omega-tail existente
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Você parece já estar em uma pasta omega-tail — veja a seção Atualização do README." >&2; exit 1; }

# 1. Extrair
[ -d omega-tail ] && echo "ℹ️ Já extraído aqui, etapa ignorada." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Mover para o home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail já existe, movimentação ignorada." || mv omega-tail ~/

# 3. Entrar no projeto
cd ~/omega-tail/

# 4. Criar o ambiente virtual
[ -f .venv/bin/activate ] && echo "ℹ️ .venv já existe, criação ignorada." || python3 -m venv .venv

# 5. Instalar as dependências (omega-lib embutida primeiro)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Tornar os lançadores executáveis
chmod +x omega-tail.sh install.sh

# 7. Gravar o token de instalação (lido pelo omega-connect; opcional)
./omega-tail.sh synchro jeton

# 8. Iniciar
./omega-tail.sh
```

No Debian, no Ubuntu e em derivadas, o módulo `venv` nem sempre é instalado com o Python:
`sudo apt install python3-venv`.

### Atualização

Os serviços do omega-tail (portão, vigilância) usam os arquivos de `~/omega-tail/var/`. Uma atualização deve
portanto **manter essa pasta no lugar**: o arquivo não contém `var/` e é extraído por cima da instalação
existente.

A partir da pasta que contém o arquivo, **diferente de `~/omega-tail`**:

```bash
# 1. Fazer backup da instalação atual (incluindo var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Extrair a nova versão por cima (var/ é preservado)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Reinstalar (dependências, lançadores, token de instalação)
cd ~/omega-tail
./install.sh

# 4. Iniciar o omega-tail novamente
./omega-tail.sh
```

Se o portão estiver ativo, **Firewall do Funnel → « Aplicar as regras »** regenera a sua configuração com a nova
versão, a quente. Se a vigilância automática estiver ativada, **Sobrevivência → « Ativar a vigilância »** a reinicia
com o novo código. O omega-connect também pode fazer a atualização (tela Updater).

### Alias Bash ou Zsh

O `install.sh` propõe o alias. Para adicioná-lo manualmente:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

O alias se chama `omega-tail`, e não `tail`, para não esconder o comando de sistema `tail`.

[↑ Sumário](#sumário)

---

## Uso

### Inicialização

```bash
cd ~/omega-tail
./omega-tail.sh

# ou simplesmente, se o alias tiver sido criado:
omega-tail
```

O lançador não pede nenhuma elevação: o omega-tail roda sob a sua conta, e o sudo só é pedido pelas ações que
precisam dele, no terminal, com o comando exibido antes.

### Primeiros passos recomendados

Para proteger um site publicado pelo Funnel, nesta ordem:

1. **Painel**: ler os alertas; **Tornar-se operador** (uma vez, via sudo) para configurar o Tailscale sem sudo.
2. **Sobrevivência → Aplicar o confinamento**: o `tailscaled` não poderá mais tomar a máquina inteira.
3. **Publicação**: publicar o site em **HTTPS na porta 443**, caminho `/`, e depois fazer o **teste de ponta a ponta**.
4. **Firewall do Funnel → Instalar o HAProxy**, depois **Ativar a proteção**, primeiro em modo **observação**.
5. Alguns dias depois, **Ataques e decisões**: se os contadores mostrarem apenas abusos, passar o portão para o
   modo **normal**.
6. Deixar os **agrupamentos** aprenderem 7 dias em observação e depois passá-los para **aplicados**.
7. **Sobrevivência → Escudo da porta WireGuard**: aplicar em observação e depois passar para ativo.
8. Para uma máquina sem ninguém diante da tela: **Sobrevivência → Ativar a vigilância**.

### Idiomas da interface

17 idiomas: francês, inglês, espanhol, português (Brasil), italiano, alemão, neerlandês, polonês, russo,
chinês, vietnamita, tailandês, indonésio, japonês, coreano, hindi, árabe.

- Escolha nas configurações (tecla `s`, « Langue / Language », rótulo que nunca é traduzido), aplicada reiniciando
  apenas a interface.
- Pontualmente: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- No console de texto do Linux (TTY), os idiomas cuja escrita não existe nas fontes do console são exibidos em
  inglês durante a sessão; o árabe é exibido da direita para a esquerda.
- O **idioma das exportações** (relatório, lista negra, logs) é configurado à parte, « Como a interface » por padrão.

### Contato e suporte

A ajuda (tecla `a`) oferece uma tela **Contato e suporte**:

- *Pagar um café* (página PayPal do desenvolvedor);
- *Contatar o suporte* (endereço de e-mail e formulário do site, exibidos em claro);
- *Declarar-me usuário (anônimo)*;
- *Verificar atualizações*.

A declaração é voluntária, desativada por padrão e enviada uma única vez. Ela serve apenas para contar os
usuários e, se desejado, o seu continente ou país (listas fechadas, nunca texto livre). Ela envia uma chave
sorteada ao acaso, o nome do software (`omega-tail`) e a sua versão, nunca nome, nome de máquina, configuração nem
endereço do tailnet. Pode ser retirada a qualquer momento na mesma tela (*Não me declarar mais*). A verificação de
atualizações apenas lê a lista das versões publicadas no site, e nunca sem um clique.

### Ligações com as outras ferramentas omega

- **omega-connect**: o `install.sh` grava um token de instalação (`var/omega-jeton.json`) que descreve a ferramenta
  e a sua versão, sem executar nada. O omega-connect o usa para o Registro, a sincronização, o reparo, as
  atualizações e a instalação. `./omega-tail.sh synchro jeton` o regrava manualmente.
- **omega-fire** (3.7.0 ou mais recente), conectado pelo omega-connect, pode aplicar e gerenciar o escudo da porta
  WireGuard; a sua lista de regras o exibe com a origem omega-tail.

### Linha de comando

Todos os comandos são escritos `./omega-tail.sh …` (ou `omega-tail …` com o alias):

| Comando | Função |
|---|---|
| `omega-tail` | A interface |
| `omega-tail etat [--format json]` | Estado do Tailscale, da máquina e alertas, em texto ou para um script |
| `omega-tail aide` | A ajuda completa em texto |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | O relatório, exibido ou salvo |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Cortar ou religar o Funnel |
| `omega-tail veille etat` | Estado da vigilância automática e as suas últimas linhas |
| `omega-tail porte etat` | Estado do portão e contadores |
| `omega-tail porte certificat [--si-besoin]` | Renovar o certificado `*.ts.net` do portão |
| `omega-tail porte groupes` | Agrupamentos: modo ataque, impressões digitais, AS, países |
| `omega-tail porte base` | Atualizar a base AS / país |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Bloquear um endereço ou uma rede (lista negra com `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Desbloquear |
| `omega-tail porte confiance ADRESSE` | Colocar em confiança |
| `omega-tail synchro jeton` | Gravar o token de instalação (omega-connect) |
| `omega-tail --version` | A versão |

### Percurso geral

1. Tela de abertura e depois o menu principal em duas colunas (TAILSCALE e PROTEÇÃO).
2. Sob o título de cada tela, a **barra de estado** resume tudo: serviço, CPU da máquina e do `tailscaled`,
   temperatura, memória, Funnel, firewall, vigilância, conexão. Ela é relida a cada 5 segundos.
3. Cada ação que altera a máquina mostra o seu comando e depois pede confirmação; o sudo é digitado no terminal e
   a interface volta em seguida.
4. As ações sensíveis (desconexão definitiva, limpeza completa da lista negra) pedem para digitar uma palavra.
5. O resultado é exibido em uma linha, verificado no estado relido.

### Navegação

- Setas para cima / para baixo: passar de um elemento a outro (linhas de uma tabela, botões).
- Tab / Shift+Tab: passar de uma área da tela a outra.
- Enter ou clique: ativar o botão escolhido; na tabela de alertas, « Corrigir ».
- `Esc`: voltar à tela anterior (no menu: sair).
- `a`: a ajuda, a partir de qualquer tela.
- `s`: as configurações, a partir de qualquer tela.
- `t`: próximo tema (salvo).
- `r`: redesenhar a tela, exibir o tamanho do terminal e reler o estado.
- `q`: sair, com confirmação.
- `Ctrl+P`: comandos (tema, captura de tela em SVG na pasta das capturas, sair).

[↑ Sumário](#sumário)

---

## Temas e terminais

Dez temas `omega-*` são compartilhados com o resto da suíte OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Alterne entre os temas com `t`, ou escolha um nas configurações (`s`); a escolha é mantida.
- As exportações HTML têm os seus próprios temas: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- O omega-tail adapta a complexidade visual ao terminal detectado por meio de um **perfil de renderização**:
  Completo, Padrão, Reduzido ou Mono (somente ASCII).

| Tamanho mínimo | Perfil | Terminais típicos |
|---|---|---|
| 120×32 ou mais | Completo | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 ou mais | Padrão | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 ou mais | Reduzido | urxvt, xterm, SSH moderno |
| abaixo de 80×24 | Mono (somente ASCII) | Linux TTY, SSH antigo |

Após um redimensionamento, `r` relê o tamanho do terminal; ele é exibido no topo, ao lado do tema.

[↑ Sumário](#sumário)

---

## Arquivos, serviços e compatibilidade

### Na pasta do omega-tail

Todo o estado do omega-tail fica em `~/omega-tail/var/`, recriado na inicialização e nunca publicado:

```text
var/
├── settings.json         configurações (idioma, temas, pastas, limites, regras do portão)
├── omega-jeton.json      token de instalação (omega-connect)
├── porte/                configuração do portão, certificado, listas de confiança e negra, base AS / país
├── veille/               log da vigilância automática
├── survie/               originais dos arquivos modificados, estado do disjuntor
├── funnel/sauvegardes/   publicação anterior a cada mudança (as 50 mais recentes)
├── exports/              relatórios, logs e listas exportados
└── screenshots/          capturas de tela (Ctrl+P)
```

### No sistema (somente se você ativar a proteção correspondente)

Cada arquivo é colocado via sudo, com o comando mostrado, e removido pela ação inversa no omega-tail.

| Arquivo ou serviço | Colocado por | Removido por |
|---|---|---|
| Serviço `omega-tail-porte` (systemd, OpenRC ou runit) e `omega-tail-porte-certificat` (timer systemd, ou uma linha marcada do seu crontab) | Ativar a proteção | Desativar a proteção |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (ou um grupo de controle fora do systemd) | Aplicar o confinamento | Remover o confinamento |
| Timers `omega-tail-retablir-*` (religamento após um corte) | Disjuntor | Fim do corte |
| Serviço `omega-tail-veille` | Ativar a vigilância | Desativar a vigilância |
| Serviço `omega-bouclier-wg`, tabela nftables, `/etc/omega-bouclier-wg/` | Escudo: Aplicar | Escudo: Remover |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Ativar o encaminhamento IP | Exclusão do arquivo |

O arquivo `override.conf` do `tailscaled`, se existir, nunca é modificado.

### Sistemas de init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Serviço `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Logs | `journalctl` | arquivos do serviço | `svlogd`, `socklog` |
| Confinamento | arquivo de complemento systemd | grupo de controle (cgroup v2) | grupo de controle (cgroup v2) |
| Corte momentâneo | timer systemd | processo destacado sob a sua conta | processo destacado sob a sua conta |
| Portão, vigilância, escudo | serviços systemd | serviços OpenRC | serviços runit |

Fora do systemd, o confinamento por grupo de controle se perde se o `tailscaled` reiniciar: um alerta propõe
então reaplicá-lo.

### IPv4 e IPv6

O portão, as listas, os agrupamentos e o escudo tratam as duas famílias. Os prefixos contados são /24 em IPv4 e
/64 em IPv6; um endereço IPv4 visto na forma `::ffff:a.b.c.d` é tratado como o endereço IPv4.

[↑ Sumário](#sumário)

---

## Segurança

O omega-tail age sobre um serviço exposto à Internet; ele foi concebido para nunca agravar a situação.

- **Nunca root**: o aplicativo, o portão HAProxy e a vigilância rodam sob a sua conta; o sudo só é pedido para
  colocar ou remover um serviço, com o comando mostrado antes.
- **Canais privados**: os sockets de administração do portão ficam em modo 600 em uma pasta 700; a sincronização
  das suas tabelas passa por um socket da mesma pasta.
- **Reversão**: cada troca do Funnel é salva em backup, verificada, e o estado anterior é restaurado em caso de
  falha.
- **Observação primeiro**: o portão, os agrupamentos e o escudo são aplicados em observação; nada é recusado
  antes que você decida.
- **O tailnet nunca é cortado**: o portão sempre admite as suas máquinas, e o disjuntor só corta o Funnel.
- **Entradas verificadas**: somente endereços ou redes na forma canônica chegam ao HAProxy; os nomes declarados
  pelas máquinas do tailnet são limpos antes de serem exibidos.
- **Auditoria**: o código foi auditado (claude-security, 2026-11-25); os 7 pontos levantados, nenhum deles
  explorável a distância por um visitante, foram corrigidos no mesmo dia.
- Teste primeiro em uma máquina de teste ou em modo observação, e use as redes de documentação RFC 5737
  para os testes IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Sumário](#sumário)

---

## Testes e qualidade

A suíte conta com **179 testes**: domínio, casos de uso, infraestrutura (com um Funnel simulado), telas Textual com
as folhas de estilo reais, sistemas de init, segurança. O código é verificado por `ruff`, `mypy` e `import-linter`
(regras das camadas). A pasta `tests/` está incluída no arquivo.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

A maioria dos testes não precisa nem do Tailscale, nem do HAProxy, nem de root.

[↑ Sumário](#sumário)

---

## Estado do projeto

### Pontos operacionais

- Pilotagem completa do Tailscale: serviço, conexão, configurações, publicação, rede, logs.
- Portão HAProxy antes do TLS, em produção desde 2026-11-23, com regras, listas, agrupamentos e modo ataque.
- Sobrevivência: confinamento, disjuntor, vigilância automática.
- Escudo da porta WireGuard, em produção desde 2026-11-24.
- Relatório e exportações TXT, HTML, JSON.
- Compatível com o omega-connect e o omega-fire.

### Limitações conhecidas

- Os serviços sob OpenRC e runit são cobertos pelos testes, mas ainda não foram validados em uma máquina real.
- O portão protege um Funnel publicado em HTTPS em uma única porta, com o caminho `/`.
- Os agrupamentos exigem um HAProxy compilado com Lua; sem Lua, o portão funciona sem eles.
- O escudo não pode ser aplicado em um kernel atualizado sem reinicialização (módulos ausentes): a tela avisa.
- Um ataque que satura a própria linha de Internet continua fora do alcance de uma ferramenta instalada na máquina.
- A vazão de um site publicado pelo Funnel continua limitada pelos retransmissores do Tailscale e pelo roteador.

[↑ Sumário](#sumário)

---

## Desinstalação

Remova primeiro, a partir do omega-tail, o que foi colocado no sistema, nesta ordem:

1. **Firewall do Funnel → Desativar a proteção** (o Funnel volta ao que era antes).
2. **Sobrevivência → Desativar a vigilância**.
3. **Sobrevivência → Escudo da porta WireGuard → Remover**.
4. **Sobrevivência → Remover o confinamento**.

Depois exclua a pasta:

```bash
rm -rf ~/omega-tail
```

Exclua manualmente as exportações colocadas em outros locais, o alias `omega-tail` de `~/.bashrc` ou `~/.zshrc` e,
se você o tiver ativado, o arquivo `/etc/sysctl.d/99-omega-tail-forwarding.conf`. O direito de operador do
Tailscale é retirado com `sudo tailscale set --operator=`.

[↑ Sumário](#sumário)

---

## Licença

O Omega-Tail é distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](../../../LICENSE) para o texto
completo.

A base AS / país usa IP Geolocation by [DB-IP](https://db-ip.com), sob a licença
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Sumário](#sumário)

---

> **Omega-Tail — Pilotar o Tailscale, proteger o Funnel.**
>
> Uma interface TUI para o Tailscale e um portão que recusa os abusos antes de qualquer criptografia.
