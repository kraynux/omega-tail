<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Gestor de control de TAILSCALE con cortafuegos integrado para FUNNEL**

OMEGA-TAIL es la herramienta de la suite OMEGA que controla **Tailscale** en una máquina y la **protege** cuando
publica un servicio en Internet mediante **Tailscale Funnel**.

> Desarrollado por [kraynux](https://github.com/kraynux) para [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Página oficial](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/es/) · [Capturas de pantalla](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interfaz, documentación, exportaciones y páginas para visitantes disponibles en **17 idiomas** — vea [Idiomas de la interfaz](#idiomas-de-la-interfaz).  
**Idiomas:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** es una aplicación TUI (Terminal User Interface) en Python construida con
[Textual](https://textual.textualize.io/). Permite gestionar y ajustar **Tailscale** en modo avanzado desde una
interfaz, sin memorizar ni una sola orden. También añade protecciones (cortafuegos, confinamiento, supervivencia…)
para el modo **Funnel**, que abre un servicio de la máquina a todo Internet.

Cada acción que modifica la máquina muestra primero su orden. La contraseña de sudo se introduce en el terminal,
acción por acción, y nada se lanza en segundo plano sin usted.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/es/omega-tail/F.png" width="32%" />
</p>

El proyecto está diseñado según los principios de la **Clean Architecture**, con `app/` como raíz de composición:
el dominio de negocio, la orquestación, la infraestructura y la interfaz están separados.

## Índice

- [Presentación](#presentación)
- [Entender Tailscale y Funnel](#entender-tailscale-y-funnel)
- [Funcionalidades](#funcionalidades)
- [Las protecciones en detalle](#las-protecciones-en-detalle)
- [Mediciones](#mediciones)
- [Arquitectura](#arquitectura)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Temas y terminales](#temas-y-terminales)
- [Archivos, servicios y compatibilidad](#archivos-servicios-y-compatibilidad)
- [Seguridad](#seguridad)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Estado del proyecto](#estado-del-proyecto)
- [Desinstalación](#desinstalación)
- [Licencia](#licencia)

---

## Presentación

### Por qué omega-tail

Tailscale Funnel publica un servicio de la máquina en Internet sin abrir ningún puerto en el router: los visitantes
pasan por los relés de Tailscale. Es sencillo y seguro en el lado de la red, pero queda una debilidad.

- **El coste del cifrado.** En el modo Funnel por defecto, es el servicio `tailscaled` de la máquina el que realiza
  el saludo (handshake) TLS de cada visitante. Medido en una máquina pequeña, supone alrededor del **80 % del coste
  de una conexión**. Unos cientos de conexiones nuevas por segundo bastan para saturar el procesador: un solo
  ordenador corriente, con un simple script, puede tumbar el sitio y la máquina.
- **Visitantes invisibles.** Los cortafuegos habituales (nftables, ufw, fail2ban) no ven a estos visitantes:
  llegan cifrados, por el túnel de Tailscale, con la dirección de un relé.
- **Ajustes dispersos.** Los ajustes de Tailscale (operador, nodo de salida, rutas, SSH, escudo…) son
  numerosos, están repartidos entre órdenes y la consola web, y algunos pueden cortar la sesión en curso.

### Objetivos

- Controlar Tailscale por completo desde una interfaz, con una frase de explicación para cada ajuste.
- Rechazar las conexiones abusivas **antes** de cualquier cifrado, viendo la dirección real de cada visitante.
- Mantener la máquina en pie bajo ataque: la administración y los demás servicios siguen siendo accesibles.
- No imponer nunca nada: proponer, mostrar la orden, preguntar y poder volver atrás.
- Funcionar en cualquier distribución Linux, con systemd, OpenRC o runit.

### Qué hace omega-tail

- Muestra el estado de Tailscale, de la máquina y de lo que está publicado, con alertas que llevan a la pantalla
  que lo corrige.
- Inicia, detiene y reinicia `tailscaled`, con una salvaguarda si su sesión pasa por Tailscale.
- Gestiona la conexión, las cuentas y todos los ajustes de `tailscale set`, verificados antes de aplicarse.
- Publica, retira, suspende y prueba los servicios de Serve y de Funnel, con copias de seguridad y restauración.
- Muestra los dispositivos del tailnet, su camino (directo o por relé), un diagnóstico de red y los registros.
- Coloca una **puerta** HAProxy entre Funnel y su sitio: reglas por dirección, por prefijo, presupuesto global,
  listas de confianza y negra, agrupaciones por huella JA4, red de origen (AS) y país, modo ataque automático.
- Confina `tailscaled`, corta Funnel durante un rato o por completo, y puede hacerlo solo gracias a una vigilancia
  automática.
- Protege el puerto WireGuard de `tailscaled` mediante una tabla nftables (escudo).
- Produce un informe de la máquina y de los ataques de los últimos 7 días, en TXT, HTML o JSON.

### Qué no hace el proyecto

- No sustituye a Tailscale: lo controla.
- No protege contra un ataque volumétrico que sature la propia línea de Internet (el router, el enlace).
- No gestiona la consola de administración web de Tailscale (política de acceso, aprobación de los nodos de salida,
  activación de Funnel para el tailnet).
- No protege un servicio publicado de otra forma que no sea Funnel: para esos puertos existe omega-fire.
- Nunca se ejecuta como root y no lanza nada en segundo plano sin su consentimiento.
- No funciona ni en Windows ni en macOS.

[↑ Índice](#índice)

---

## Entender Tailscale y Funnel

omega-tail presupone algunas nociones de Tailscale. Esta parte las reúne, sin presuponer nada más.

### El vocabulario

| Término | Qué es |
|---|---|
| **Tailnet** | Su red privada Tailscale: todas las máquinas conectadas a la misma cuenta (o a la misma organización). Cada máquina recibe en ella una dirección en `100.x.y.z` (rango 100.64.0.0/10) y una dirección IPv6 en `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | El servicio (demonio) que se ejecuta en la máquina: mantiene el túnel cifrado WireGuard, la pila de red de Tailscale y, para Serve y Funnel, el relé hacia sus servicios. |
| **`tailscale`** | La orden que controla `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail la usa por usted. |
| **WireGuard** | El protocolo de túnel cifrado usado entre las máquinas. Para ello, `tailscaled` escucha en un puerto UDP (41641 por defecto), a menudo abierto por el router (UPnP). |
| **Relé DERP (DERP relay)** | Servidores de Tailscale que retransmiten el tráfico cuando dos máquinas no pueden comunicarse directamente (NAT difícil). El camino «directo» es más rápido. |
| **MagicDNS** | Los nombres de las máquinas del tailnet, con la forma `maquina.nombre-del-tailnet.ts.net`. |
| **Serve** | Publicar un servicio local (un sitio, una API…) **solo para el tailnet**, en HTTPS con un certificado `*.ts.net` válido. |
| **Funnel** | Publicar un servicio local **para todo Internet**, en la dirección `https://maquina.nombre-del-tailnet.ts.net`. Solo se pueden abrir los puertos 443, 8443 y 10000. |
| **Relé de Funnel (Funnel relay)** | Los servidores de Tailscale que reciben a los visitantes de Internet y los hacen entrar en su tailnet (aparecen como «funnel-ingress-node»). |
| **Operador (operator)** | Una cuenta Linux autorizada a ajustar Tailscale sin sudo (`tailscale set --operator=…`). omega-tail lo propone una vez, mediante sudo. |
| **Nodo de salida (exit node)** | Una máquina del tailnet por la que otra hace pasar todo su tráfico de Internet (como una VPN). Debe aprobarse en la consola de Tailscale. |
| **Subred anunciada (subnet router)** | Una red local (por ejemplo `192.168.1.0/24`) que una máquina hace accesible al resto del tailnet. |
| **Escudo (shields up)** | Ajuste de Tailscale que rechaza todas las conexiones entrantes procedentes del tailnet. |
| **SSH de Tailscale (Tailscale SSH)** | Un servidor SSH proporcionado por Tailscale, autorizado por la política del tailnet. |
| **Cabecera PROXY v2** | Una cabecera corta añadida al principio de una conexión para transmitir la dirección real del visitante a quien la recibe. |
| **Huella JA4** | Una firma de la manera en que un programa abre una conexión TLS: un navegador y una herramienta de ataque no tienen la misma. |
| **AS (sistema autónomo)** | La red de origen de una dirección: proveedor de acceso, empresa de alojamiento, nube. |

### El camino de un visitante

**Funnel por defecto, sin omega-tail.** `tailscaled` lo hace todo: descifra el túnel WireGuard, realiza el saludo
TLS del visitante y luego retransmite la petición en HTTP a su sitio. Ningún cortafuegos de la máquina ve al
visitante, y cada conexión nueva le cuesta cara a `tailscaled`.

```text
Visitante ──HTTPS──▶ Relé de Funnel ──WireGuard──▶ tailscaled (TLS + relé HTTP) ──HTTP──▶ su sitio
                     (Tailscale)                   └── todo el coste está aquí
```

**Funnel con la puerta de omega-tail.** Funnel pasa a modo TCP: `tailscaled` ya no hace TLS, transmite el
flujo todavía cifrado a la puerta, precedido de la dirección real del visitante (cabecera PROXY v2). La puerta
decide **antes** de cualquier cifrado: una conexión rechazada casi no cuesta nada, y solo se descifran las
conexiones admitidas, mediante OpenSSL, más rápido que el TLS de `tailscaled`.

```text
Visitante ──HTTPS──▶ Relé de Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                        │
                                                        ▼
                                         Puerta omega-tail (HAProxy, 127.0.0.1)
                                         ├── rechazo antes de TLS: lista negra, tasa, presupuesto, nombre de destino, agrupaciones
                                         └── admitido: TLS (certificado *.ts.net) ──HTTP──▶ su sitio
```

La puerta solo escucha en el bucle local de la máquina y se ejecuta con su cuenta. Las máquinas de su tailnet
siempre se admiten, antes de cualquier regla: solo se filtran los visitantes de Funnel.

### Qué debe permitir Tailscale (consola de administración)

Estos ajustes se hacen una vez, en la consola web de Tailscale; omega-tail no los cambia.

- **MagicDNS** y los **certificados HTTPS** activados para el tailnet (necesarios para Serve, para Funnel y para el
  certificado de la puerta).
- **Funnel autorizado** para la máquina en la política de acceso del tailnet (atributo `funnel`).
- Para un nodo de salida o subredes anunciadas: su **aprobación** en la consola.

[↑ Índice](#índice)

---

## Funcionalidades

El menú principal tiene dos columnas de seis: **TAILSCALE** para controlar, **PROTECCIÓN** para defender.

### TAILSCALE

#### 1. Panel de control

- **Tailscale**: servicio, estado de la conexión, versión en ejecución e instalada, nombre de la máquina, direcciones,
  cuenta, dispositivos en línea, caducidad de la clave, operador, nodo de salida ofrecido y utilizado, subredes
  anunciadas.
- **Máquina**: CPU de toda la máquina, carga por núcleo, temperatura, memoria, CPU y memoria de `tailscaled`,
  confinamiento, y luego el estado de las protecciones (Funnel, cortafuegos y modo ataque, lista negra, vigilancia,
  escudo).
- **Publicación**: cada puerto publicado, para Internet (Funnel) o para el tailnet (Serve), su modo y su destino.
- **Alertas**, de la más grave a la menos grave, con «Corregir», que abre la pantalla correspondiente. Por ejemplo:
  servicio detenido, actualización instalada pero no aplicada, clave que caduca, Funnel publicado sin protección,
  temperatura elevada, `tailscaled` demasiado voraz o no confinado, lista negra que crece.
- Valores en verde, naranja o rojo según umbrales (CPU, carga, temperatura, memoria, `tailscaled`).

#### 2. Servicio tailscaled

- Estado visto por el sistema de init, versión en ejecución e instalada, orden de lanzamiento, archivos
  complementarios (drop-in), confinamiento.
- **Iniciar**, **Detener**, **Reiniciar** (por ejemplo, para aplicar una actualización ya instalada).
- **Salvaguarda**: si su sesión pasa por Tailscale (SSH a través del tailnet), Detener pide una segunda
  confirmación, porque ya no podría volver a lanzarlo.
- **Corregir el arranque**: detecta un archivo complementario que lanza `tailscale up` al arrancar y que corre el
  riesgo de sacar la máquina del tailnet en el primer cambio de ajuste; la corrección se muestra y se conserva el
  original.

#### 3. Conexión y ajustes

- **Conectarse**, **Desconectarse**, **Añadir una cuenta**, **Cambiar de cuenta**, **Desconexión definitiva**
  (hay que escribir el nombre de la máquina).
- **Todos los ajustes de `tailscale set`**, cada uno con su frase de explicación: nombre y alias de la máquina,
  rutas, DNS del tailnet, escudo, filtrado con estado, modo netfilter, nodo de salida, acceso a la red local,
  ofrecer la máquina como nodo de salida, subredes anunciadas, SSH de Tailscale, interfaz web, actualizaciones,
  relé entre pares, operador.
- Durante la introducción, un recuadro muestra **antes → después** y la orden; tras aplicar, cada valor releído se
  marca con ✔ (tenido en cuenta) o ✖ (no).
- Un aviso indica cuándo un cambio puede cortar una sesión que pasa por Tailscale.
- **Reenvío IP**: se activa con un botón cuando la máquina sirve de nodo de salida o anuncia subredes.

#### 4. Publicación

- Todo lo que publica la máquina: puerto, público (Funnel) o tailnet (Serve), modo, ruta, destino, protección.
- **Publicar** un servicio local en HTTPS, HTTP, TCP o TLS terminado; **Retirar**; **Suspender Funnel** y
  **Restablecer Funnel** (de forma idéntica).
- **Prueba de extremo a extremo**: una conexión real, como un visitante (respuesta, tiempo, certificado, versión
  de TLS).
- **Copias de seguridad**: el estado anterior a cada cambio (las 50 más recientes), restaurables.
- Cada cambio se verifica; en caso de discrepancia, la publicación se reconstruye; si no, se restablece el estado
  anterior.

#### 5. Red y dispositivos

- **Dispositivos** del tailnet: sistema, en línea o no, camino (directo o por relé), última vez visto, dirección,
  tráfico intercambiado; los relés de Funnel de Tailscale están ocultos por defecto.
- **Ping de Tailscale** (camino y latencia), **¿Quién es?** (a quién pertenece una dirección del tailnet).
- **Diagnóstico de red**: UDP, IPv4 / IPv6, tipo de NAT, apertura de puerto por el router (UPnP, NAT-PMP, PCP),
  relé más cercano y latencias.
- **DNS**, **bloqueo del tailnet** (tailnet lock) y **contadores internos** de Tailscale.
- Solo lectura: nada en esta pantalla cambia un ajuste.

#### 6. Registros

- El registro de `tailscaled` (journalctl, o los archivos del servicio fuera de systemd) y el de la puerta, filtrables
  y exportables.
- Cada información tiene su color, tomado del tema: fecha, proceso, categoría del mensaje (control, red, DNS, motor
  WireGuard), direcciones en negrita, errores en rojo, avisos en naranja; para la puerta, motivo del rechazo,
  agrupación, AS y país.

### PROTECCIÓN

#### 7. Cortafuegos Funnel

- **Instalar HAProxy** mediante el gestor de paquetes de la distribución (pacman, apt, dnf, zypper, apk, xbps,
  emerge).
- **Activar la protección**: certificado `*.ts.net`, listas, configuración verificada, servicio de la puerta,
  conmutación de Funnel y luego prueba desde Internet; en caso de fallo, la publicación original se restablece de
  inmediato.
- **Desactivar la protección**: Funnel se restablece exactamente como antes, verificado.
- **Reglas** aplicadas en caliente, modo **observación** para ajustar los umbrales sin riesgo, **agrupaciones**
  (vea [Las protecciones en detalle](#las-protecciones-en-detalle)).
- **Actualizar la base** AS / país (DB-IP Lite), en un proceso aparte.

#### 8. Supervivencia

- **Confinamiento de `tailscaled`**: límite de CPU, peso y prioridad, opción de prioridad para el acceso SSH.
- **Disyuntor de Funnel**: umbrales de CPU y de temperatura, corte de 10 minutos (restablecimiento automático) o
  total.
- **Vigilancia automática**: lo mismo sin nadie delante de la pantalla.
- **Escudo del puerto WireGuard**: botón hacia su pantalla (observación, activo, colocar, volver a colocar, retirar,
  delegar).

#### 9. Ataques y decisiones

- Contadores de la puerta (recibidas, rechazadas antes del cifrado, admitidas, en curso) y direcciones más activas,
  releídos cada 2 segundos, con el país, el AS y el estado de cada dirección.
- **Bloquear**, **Lista negra**, **Desbloquear**, **Confianza**: se aplica de inmediato, sin reiniciar la puerta;
  la notificación indica en una línea la acción y la situación de la dirección.
- Vistas **Huellas**, **AS** y **Países**; estado del modo ataque y conexiones rechazadas por las agrupaciones.
- **Gestión de la lista negra**: lista completa con fecha de adición y origen, adición, eliminación, importación de
  un archivo TXT (duplicados, redes ya cubiertas y direcciones del tailnet descartados), purgas con vista previa
  (por antigüedad, las N más antiguas, un rango de líneas, un origen, todo), exportaciones TXT (reimportable), HTML
  y JSON. Límite de 50 000 entradas.

#### 10. Informe

- Todo lo que omega-tail sabe de la máquina, en hechos: Tailscale, publicación, máquina, cortafuegos,
  supervivencia, alertas, y los **ataques de los últimos 7 días** leídos en el registro de la puerta.
- **Privacidad**: por defecto, sin la cuenta de Tailscale ni los nombres y direcciones de los dispositivos del
  tailnet, para poder enviarlo a alguien.
- Exportaciones **TXT**, **HTML** (tema a elegir) y **JSON**; **Ver las exportaciones** abre la carpeta en el
  navegador.

#### 11. Ajustes

- Idioma de la interfaz y de las exportaciones, tema de la interfaz y de las exportaciones, carpetas de las
  exportaciones y de las capturas de pantalla, y su purga.

#### 12. Ayuda

- Una sección por pantalla, los atajos, la línea de órdenes y **Contacto y soporte**.

[↑ Índice](#índice)

---

## Las protecciones en detalle

Cada protección responde a una amenaza concreta; ninguna se impone.

| Protección | Contra qué | Dónde |
|---|---|---|
| Puerta (reglas) | Ráfagas desde una o pocas direcciones, conexiones que no apuntan al sitio | Cortafuegos Funnel |
| Agrupaciones | Ataques con direcciones dispersas (miles de direcciones, una conexión cada una) | Cortafuegos Funnel |
| Lista negra | Direcciones y redes conocidas por atacar, conservadas en el tiempo | Ataques y decisiones |
| Confinamiento | `tailscaled` acaparando toda la máquina bajo ataque | Supervivencia |
| Disyuntor | Máquina saturada pese a todo: cortar Funnel durante un rato | Supervivencia |
| Vigilancia automática | Lo mismo, sin nadie delante de la pantalla | Supervivencia |
| Escudo WireGuard | Avalancha de paquetes UDP en el puerto de `tailscaled`, con Funnel abierto o no | Supervivencia |

### La puerta (Cortafuegos Funnel)

Las reglas se aplican en este orden, todas antes del cifrado:

1. **Máquinas del tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): siempre admitidas.
2. **Lista de confianza**: nunca limitada. **Lista negra**: rechazada hasta su retirada.
3. **Tasa por dirección** (40 conexiones / 10 s por defecto): por encima, la dirección se bloquea durante el tiempo
   elegido (60 min por defecto).
4. **Tasa por prefijo** /24 en IPv4, /64 en IPv6.
5. **Presupuesto global** de conexiones admitidas por segundo: el procesador nunca se ve desbordado.
6. **Nombre de destino**: se rechaza una conexión que no apunta al nombre de la máquina.

El certificado `*.ts.net` de la puerta se solicita a Tailscale, se verifica cada día y se renueva en caliente
30 días antes de su vencimiento. El modo **observación** lo cuenta todo sin rechazar nada.

### Las agrupaciones (huellas, AS, países)

Frente a un ataque con direcciones dispersas, las reglas por dirección solo ven cada dirección una vez. Por eso la
puerta clasifica también a cada cliente por su **huella JA4**, su **AS** y su **país**, y cuenta la tasa de cada
grupo.

- **Modo ataque automático**: por encima de 80 conexiones entrantes por segundo (ajustable), la puerta pasa sola a
  modo ataque, y sale de él tras 5 minutos de calma.
- Solo en modo ataque: se rechaza una huella desconocida que se dispara, un AS de alojamiento o de nube (lista
  modificable) o un país de su lista (vacía por defecto) que supera su tasa.
- Los **navegadores habituales** (Chrome, Edge, Firefox) nunca se ven afectados por estas reglas; los **clientes
  conocidos** (admitidos en las últimas 24 h) pasan antes que el presupuesto global.
- **Aprendizaje**: durante 7 días, la puerta aprende las huellas habituales de su sitio (nunca durante un
  ataque); hasta entonces, las agrupaciones permanecen en observación.
- Fuera de un ataque, se clasifica una conexión de cada diez; durante un ataque, todas.
- La base AS / país es **DB-IP Lite**, descargada y actualizada una vez al mes.

### La supervivencia

- **Confinamiento**: un archivo complementario aparte limita `tailscaled` (por ejemplo, a un núcleo entero en una
  máquina de 4 hilos) y baja su prioridad. Su propia configuración nunca se modifica.
- **Disyuntor**: cuando `tailscaled` se mantiene por encima del umbral de CPU (80 % de un núcleo durante 60 s por
  defecto) o la temperatura alcanza 85 °C, omega-tail propone cortar Funnel 10 minutos (restablecimiento
  automático, idéntico, incluso con omega-tail cerrado), cortarlo por completo o esperar. El tailnet nunca se corta.
- **Vigilancia automática** (desactivada por defecto): un servicio con su cuenta corta Funnel por sí solo tras tres
  rebasamientos, 15 minutos la primera vez, 30 la segunda y luego una hora, y lo restablece por sí solo.

### El escudo del puerto WireGuard

`tailscaled` consume alrededor de un núcleo de procesador por cada 100 000 paquetes por segundo recibidos en su
puerto UDP, incluso inválidos. El escudo es una tabla nftables colocada delante de él, en las tarjetas de red:

- los **pares conocidos** (aquellos a los que `tailscaled` escribe) nunca se limitan;
- los saludos (handshakes) se limitan a 20 por segundo y por origen;
- los demás orígenes tienen un presupuesto (500 paquetes por segundo cada uno, 5000 en total);
- los paquetes que no son WireGuard se rechazan.

Se coloca primero en **observación** y luego en **activo**. Si está vinculado mediante omega-connect,
**omega-fire** (3.7.0 o más reciente) puede colocarlo y gestionarlo en lugar de omega-tail: es la misma tabla, que
cambia de manos sin que se toque.

[↑ Índice](#índice)

---

## Mediciones

Las decisiones de omega-tail proceden de mediciones, en máquinas de la misma generación que las que protege
(procesadores de 2010 a 2016, en su mayoría sin aceleración AES).

| Medición | Resultado |
|---|---|
| Parte del TLS en el coste de una conexión Funnel por defecto | alrededor del 80 % |
| Coste de una conexión **rechazada** por la puerta, comparado con Funnel por defecto | **4,6 veces menos** |
| Coste de una conexión **admitida** por la puerta, comparado con Funnel por defecto | **2 veces menos** |
| Rendimiento con la puerta, conexiones mantenidas abiertas (comparado con un TLS en Go como el de `tailscaled`) | **+15 %** de peticiones, −20 % de CPU |
| Escudo WireGuard: avalancha que ocupaba un núcleo entero de `tailscaled` | **1 %** de un núcleo |
| Memoria de los servicios (puerta, vigilancia, escudo) | alrededor de 67 MB |

Así pues, la puerta no degrada el rendimiento de un sitio: en estas máquinas, es el propio cifrado el que limita,
con o sin omega-tail, y en producción Funnel pasa de todos modos por los relés de Tailscale y por el router.

[↑ Índice](#índice)

---

## Arquitectura

```text
src/omega_tail/
├── app/              Raíz de composición: ensambla las capas, punto de entrada (interfaz, línea de órdenes)
├── core/             Constantes compartidas
├── domain/           Lógica de negocio pura: reglas de la puerta, alertas, disyuntor, vigilancia, lista negra…
├── application/      Casos de uso: publicación, cortafuegos, supervivencia, informe, ajustes
├── ports/            Contratos (Protocol) esperados por la aplicación
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, registros, exportaciones, scripts Lua
├── interfaces/       tui/ (Textual), cli/ (línea de órdenes), shared/ (ayuda, informe, presentación)
└── shared/           Idiomas (gettext)
```

### Principios de diseño

- `domain/` no contiene ni lecturas ni escrituras: todo en él puede probarse sin máquina.
- `application/` orquesta los casos de uso mediante el dominio y los puertos; la interfaz y la línea de órdenes
  llaman a los mismos casos de uso.
- Solo `infrastructure.commands` e `infrastructure.privileged` lanzan órdenes; la interfaz nunca las lanza
  directamente. Estas reglas se verifican automáticamente (import-linter).
- La interfaz se apoya en [omega-lib](https://github.com/kraynux), la biblioteca compartida por toda la suite
  OMEGA (temas, detección del terminal, idiomas, contacto y soporte, escudo WireGuard). No está publicada en
  PyPI: va incluida en el archivo (`vendor/omega-lib/`).
- Toda llamada lenta (Tailscale, HAProxy, disco, red) se ejecuta como tarea en segundo plano: la interfaz nunca se
  congela.

[↑ Índice](#índice)

---

## Requisitos previos

### Sistema

- Linux, cualquier distribución (probado en Arch Linux y derivadas).
- Python 3.10 o superior, con el módulo `venv`.
- Un sistema de init: **systemd**, **OpenRC** o **runit**.
- `sudo` para las acciones que modifican la máquina (solicitado acción por acción, nunca al lanzar).
- Un terminal de al menos 80×24 (vea [Temas y terminales](#temas-y-terminales)).

### Tailscale

- **Tailscale** instalado y conectado (cliente `tailscale` y servicio `tailscaled`); probado con la versión 1.104.
- Para Funnel: MagicDNS, certificados HTTPS y Funnel autorizados en la consola de Tailscale (vea
  [Qué debe permitir Tailscale](#qué-debe-permitir-tailscale-consola-de-administración)).

### Dependencias de Python

Instaladas por `install.sh` en un entorno virtual:

- `textual`: la interfaz.
- `omega-lib`: biblioteca compartida de la suite OMEGA, incluida en el archivo.

### Componentes obligatorios y opcionales

omega-tail detecta lo que está presente y solo activa lo que se puede usar.

| Componente | Función | Estado |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Todo lo que omega-tail controla | **Obligatorio** |
| Python 3.10+, `textual`, `omega-lib` | La aplicación | **Obligatorio** |
| systemd, OpenRC o runit | Servicios de la puerta, de la vigilancia, del escudo | **Obligatorio** (uno de los tres) |
| HAProxy 3.x | La puerta del Cortafuegos Funnel | Opcional (instalable desde omega-tail) |
| HAProxy con Lua | Las agrupaciones (huellas, AS, países) | Opcional (caso de las distribuciones habituales) |
| nftables (núcleo con `nft_limit`) | El escudo del puerto WireGuard | Opcional |
| Lectura del diario del sistema (grupo `systemd-journal`, `adm` o `wheel`) | Registros, informe de los ataques | Recomendado |
| Navegador y escritorio | «Ver las exportaciones» en el navegador (si no, lectura en omega-tail) | Opcional |
| omega-connect | Registro, sincronización, actualizaciones de la suite | Opcional |
| omega-fire 3.7.0+ | Gestión del escudo WireGuard desde omega-fire | Opcional |

[↑ Índice](#índice)

---

## Instalación

El archivo oficial se proporciona en formato `.tar.gz`. Verifique su integridad antes de la instalación, con el
archivo `sha.txt` publicado junto a él:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Estos tres métodos sirven para una primera instalación.** Si `~/omega-tail` ya existe, use la
> sección [Actualización](#actualización). No vuelva a lanzar nunca estas órdenes desde dentro de una carpeta
> `omega-tail` existente: `tar` crearía un `omega-tail/omega-tail/` anidado.

Ningún paso de la instalación requiere derechos de root: omega-tail se ejecuta como usuario normal.

### Método 1 — script de instalación

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Parece que ya está dentro de una carpeta omega-tail — vea la sección Actualización del README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Ya extraído aquí, paso omitido." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail ya existe, movimiento omitido." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

El script crea el entorno virtual, instala las dependencias (primero omega-lib incluida), hace ejecutables los
lanzadores, escribe el token de instalación que lee omega-connect y propone el alias `omega-tail`. Puede volver a
lanzarse sin riesgo.

### Método 2 — instalación completa resiliente

Esta orden puede volver a lanzarse: omite los pasos ya realizados.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Parece que ya está dentro de una carpeta omega-tail — vea la sección Actualización del README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail ya existe, extracción omitida." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv ya existe, paso omitido." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail instalado. Ejecute ./omega-tail.sh."
```

### Método 3 — instalación detallada

```bash
# 0. Verificar que no se relanza desde dentro de un omega-tail existente
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Parece que ya está dentro de una carpeta omega-tail — vea la sección Actualización del README." >&2; exit 1; }

# 1. Extraer
[ -d omega-tail ] && echo "ℹ️ Ya extraído aquí, paso omitido." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Mover al home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail ya existe, movimiento omitido." || mv omega-tail ~/

# 3. Entrar en el proyecto
cd ~/omega-tail/

# 4. Crear el entorno virtual
[ -f .venv/bin/activate ] && echo "ℹ️ .venv ya existe, creación omitida." || python3 -m venv .venv

# 5. Instalar las dependencias (primero omega-lib incluida)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Hacer ejecutables los lanzadores
chmod +x omega-tail.sh install.sh

# 7. Escribir el token de instalación (leído por omega-connect; opcional)
./omega-tail.sh synchro jeton

# 8. Lanzar
./omega-tail.sh
```

En Debian, Ubuntu y derivadas, el módulo `venv` no siempre se instala con Python:
`sudo apt install python3-venv`.

### Actualización

Los servicios de omega-tail (puerta, vigilancia) usan los archivos de `~/omega-tail/var/`. Por tanto, una
actualización debe **dejar esta carpeta en su sitio**: el archivo no contiene `var/` y se extrae encima de la
instalación existente.

Desde la carpeta que contiene el archivo, **distinta de `~/omega-tail`**:

```bash
# 1. Hacer una copia de seguridad de la instalación actual (var/ incluido)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Extraer la nueva versión encima (var/ se conserva)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Reinstalar (dependencias, lanzadores, token de instalación)
cd ~/omega-tail
./install.sh

# 4. Volver a lanzar omega-tail
./omega-tail.sh
```

Si la puerta está activa, **Cortafuegos Funnel → «Aplicar las reglas»** regenera su configuración con la nueva
versión, en caliente. Si la vigilancia automática está activada, **Supervivencia → «Activar la vigilancia»** la
relanza con el código nuevo. omega-connect también puede realizar la actualización (pantalla Updater).

### Alias de Bash o Zsh

`install.sh` propone el alias. Para añadirlo a mano:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

El alias se llama `omega-tail`, y no `tail`, para no ocultar la orden del sistema `tail`.

[↑ Índice](#índice)

---

## Uso

### Lanzamiento

```bash
cd ~/omega-tail
./omega-tail.sh

# o simplemente, si se creó el alias:
omega-tail
```

El lanzador no pide ninguna elevación: omega-tail se ejecuta con su cuenta, y sudo solo lo piden las acciones que
lo necesitan, en el terminal, con la orden mostrada antes.

### Primeros pasos recomendados

Para proteger un sitio publicado mediante Funnel, en este orden:

1. **Panel de control**: leer las alertas; **Convertirse en operador** (una vez, mediante sudo) para ajustar
   Tailscale sin sudo.
2. **Supervivencia → Aplicar el confinamiento**: `tailscaled` ya no podrá acaparar toda la máquina.
3. **Publicación**: publicar el sitio en **HTTPS en el puerto 443**, ruta `/`, y luego hacer la **prueba de extremo
   a extremo**.
4. **Cortafuegos Funnel → Instalar HAProxy**, y luego **Activar la protección**, primero en modo **observación**.
5. Unos días más tarde, **Ataques y decisiones**: si los contadores solo muestran abusos, pasar la puerta a
   modo **normal**.
6. Dejar que las **agrupaciones** aprendan 7 días en observación, y luego pasarlas a **aplicadas**.
7. **Supervivencia → Escudo del puerto WireGuard**: colocarlo en observación y luego pasarlo a activo.
8. Para una máquina sin nadie delante de la pantalla: **Supervivencia → Activar la vigilancia**.

### Idiomas de la interfaz

17 idiomas: francés, inglés, español, portugués (Brasil), italiano, alemán, neerlandés, polaco, ruso,
chino, vietnamita, tailandés, indonesio, japonés, coreano, hindi, árabe.

- Se elige en los ajustes (tecla `s`, «Langue / Language», etiqueta que nunca se traduce), aplicado reiniciando
  solo la interfaz.
- Puntualmente: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- En la consola de texto de Linux (TTY), los idiomas cuya escritura no existe en las fuentes de la consola
  se muestran en inglés durante la sesión; el árabe se muestra de derecha a izquierda.
- El **idioma de las exportaciones** (informe, lista negra, registros) se ajusta aparte, «Como la interfaz» por
  defecto.

### Contacto y soporte

La ayuda (tecla `a`) ofrece una pantalla **Contacto y soporte**:

- *Invitar a un café* (página PayPal del desarrollador);
- *Contactar con el soporte* (dirección de correo y formulario del sitio, mostrados en claro);
- *Declararme usuario (anónimo)*;
- *Buscar actualizaciones*.

La declaración es voluntaria, está desactivada por defecto y se envía una sola vez. Solo sirve para contar a los
usuarios y, si se desea, su continente o su país (listas cerradas, nunca texto libre). Envía una clave elegida al
azar, el nombre del programa (`omega-tail`) y su versión; nunca un nombre, un nombre de máquina, un ajuste ni una
dirección del tailnet. Retirada en cualquier momento desde la misma pantalla (*Dejar de declararme*). La búsqueda
de actualizaciones solo lee la lista de versiones publicadas en el sitio, y nunca sin un clic.

### Vínculos con las demás herramientas omega

- **omega-connect**: `install.sh` escribe un token de instalación (`var/omega-jeton.json`) que describe la
  herramienta y su versión, sin ejecutar nada. omega-connect lo usa para el Registro, la sincronización, la
  reparación, las actualizaciones y la instalación. `./omega-tail.sh synchro jeton` lo reescribe a mano.
- **omega-fire** (3.7.0 o más reciente), vinculado mediante omega-connect, puede colocar y gestionar el escudo del
  puerto WireGuard; su lista de reglas lo muestra con el origen omega-tail.

### Línea de órdenes

Todas las órdenes se escriben `./omega-tail.sh …` (u `omega-tail …` con el alias):

| Orden | Función |
|---|---|
| `omega-tail` | La interfaz |
| `omega-tail etat [--format json]` | Estado de Tailscale, de la máquina y alertas, en texto o para un script |
| `omega-tail aide` | La ayuda completa en texto |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | El informe, mostrado o guardado |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Cortar o restablecer Funnel |
| `omega-tail veille etat` | Estado de la vigilancia automática y sus últimas líneas |
| `omega-tail porte etat` | Estado de la puerta y contadores |
| `omega-tail porte certificat [--si-besoin]` | Renovar el certificado `*.ts.net` de la puerta |
| `omega-tail porte groupes` | Agrupaciones: modo ataque, huellas, AS, países |
| `omega-tail porte base` | Actualizar la base AS / país |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Bloquear una dirección o una red (lista negra con `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Desbloquear |
| `omega-tail porte confiance ADRESSE` | Poner en confianza |
| `omega-tail synchro jeton` | Escribir el token de instalación (omega-connect) |
| `omega-tail --version` | La versión |

### Recorrido general

1. Pantalla de inicio y luego el menú principal en dos columnas (TAILSCALE y PROTECCIÓN).
2. Bajo el título de cada pantalla, la **banda de estado** lo resume todo: servicio, CPU de la máquina y de
   `tailscaled`, temperatura, memoria, Funnel, cortafuegos, vigilancia, conexión. Se relee cada 5 segundos.
3. Cada acción que modifica la máquina muestra su orden y luego pide confirmación; sudo se introduce en el
   terminal y después la interfaz vuelve.
4. Las acciones sensibles (desconexión definitiva, purga completa de la lista negra) piden escribir una palabra.
5. El resultado se muestra en una línea, verificado sobre el estado releído.

### Navegación

- Flechas arriba / abajo: pasar de un elemento a otro (filas de una tabla, botones).
- Tab / Mayús+Tab: pasar de una zona de la pantalla a otra.
- Intro o clic: activar el botón elegido; en la tabla de alertas, «Corregir».
- `Esc`: volver a la pantalla anterior (en el menú: salir).
- `a`: la ayuda, desde cualquier pantalla.
- `s`: los ajustes, desde cualquier pantalla.
- `t`: tema siguiente (guardado).
- `r`: redibujar la pantalla, mostrar el tamaño del terminal y releer el estado.
- `q`: salir, con confirmación.
- `Ctrl+P`: órdenes (tema, captura de pantalla en SVG en la carpeta de capturas, salir).

[↑ Índice](#índice)

---

## Temas y terminales

Diez temas `omega-*` se comparten con el resto de la suite OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Cambie entre temas con `t`, o elija uno en los ajustes (`s`); la elección se conserva.
- Las exportaciones HTML tienen sus propios temas: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`,
  `light-alt`.
- omega-tail adapta la complejidad visual al terminal detectado mediante un **perfil de renderizado**: Completo,
  Estándar, Reducido o Mono (solo ASCII).

| Tamaño mínimo | Perfil | Terminales típicos |
|---|---|---|
| 120×32 o más | Completo | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 o más | Estándar | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 o más | Reducido | urxvt, xterm, SSH moderno |
| por debajo de 80×24 | Mono (solo ASCII) | Linux TTY, SSH antiguo |

Tras un redimensionamiento, `r` relee el tamaño del terminal; se muestra arriba, junto al tema.

[↑ Índice](#índice)

---

## Archivos, servicios y compatibilidad

### En la carpeta de omega-tail

Todo el estado de omega-tail está en `~/omega-tail/var/`, recreado al arrancar y nunca publicado:

```text
var/
├── settings.json         ajustes (idioma, temas, carpetas, umbrales, reglas de la puerta)
├── omega-jeton.json      token de instalación (omega-connect)
├── porte/                configuración de la puerta, certificado, listas de confianza y negra, base AS / país
├── veille/               registro de la vigilancia automática
├── survie/               originales de los archivos modificados, estado del disyuntor
├── funnel/sauvegardes/   publicación anterior a cada cambio (las 50 más recientes)
├── exports/              informes, registros y listas exportados
└── screenshots/          capturas de pantalla (Ctrl+P)
```

### En el sistema (solo si activa la protección correspondiente)

Cada archivo se coloca mediante sudo, con la orden mostrada, y se retira con la acción inversa en omega-tail.

| Archivo o servicio | Colocado por | Retirado por |
|---|---|---|
| Servicio `omega-tail-porte` (systemd, OpenRC o runit) y `omega-tail-porte-certificat` (temporizador systemd, o una línea marcada de su crontab) | Activar la protección | Desactivar la protección |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (o un grupo de control fuera de systemd) | Aplicar el confinamiento | Retirar el confinamiento |
| Temporizadores `omega-tail-retablir-*` (restablecimiento tras un corte) | Disyuntor | Fin del corte |
| Servicio `omega-tail-veille` | Activar la vigilancia | Desactivar la vigilancia |
| Servicio `omega-bouclier-wg`, tabla nftables, `/etc/omega-bouclier-wg/` | Escudo: Colocar | Escudo: Retirar |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Activar el reenvío IP | Eliminación del archivo |

El archivo `override.conf` de `tailscaled`, si existe, nunca se modifica.

### Sistemas de init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Servicio `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Registros | `journalctl` | archivos del servicio | `svlogd`, `socklog` |
| Confinamiento | archivo complementario de systemd | grupo de control (cgroup v2) | grupo de control (cgroup v2) |
| Corte momentáneo | temporizador systemd | proceso separado con su cuenta | proceso separado con su cuenta |
| Puerta, vigilancia, escudo | servicios systemd | servicios OpenRC | servicios runit |

Fuera de systemd, el confinamiento por grupo de control se pierde si `tailscaled` se reinicia: una alerta propone
entonces volver a aplicarlo.

### IPv4 e IPv6

La puerta, las listas, las agrupaciones y el escudo tratan las dos familias. Los prefijos contados son /24 en
IPv4 y /64 en IPv6; una dirección IPv4 vista con la forma `::ffff:a.b.c.d` se trata como la dirección IPv4.

[↑ Índice](#índice)

---

## Seguridad

omega-tail actúa sobre un servicio expuesto a Internet; se ha diseñado para no agravar nunca la situación.

- **Nunca root**: la aplicación, la puerta HAProxy y la vigilancia se ejecutan con su cuenta; sudo solo se pide
  para colocar o retirar un servicio, con la orden mostrada antes.
- **Canales privados**: los sockets de administración de la puerta están en modo 600 dentro de una carpeta 700; la
  sincronización de sus tablas pasa por un socket de la misma carpeta.
- **Vuelta atrás**: cada conmutación de Funnel se guarda, se verifica, y el estado anterior se restablece en caso
  de fallo.
- **Primero la observación**: la puerta, las agrupaciones y el escudo se colocan en observación; no se rechaza nada
  antes de que usted lo haya decidido.
- **El tailnet nunca se corta**: la puerta siempre admite sus máquinas, y el disyuntor solo corta Funnel.
- **Entradas verificadas**: solo llegan a HAProxy direcciones o redes en forma canónica; los nombres declarados
  por las máquinas del tailnet se limpian antes de mostrarse.
- **Auditoría**: el código ha sido auditado (claude-security, 2026-11-25); los 7 puntos detectados, ninguno de
  ellos explotable a distancia por un visitante, se corrigieron el mismo día.
- Pruebe primero en una máquina de pruebas o en modo observación, y use las redes de documentación RFC 5737
  para las pruebas IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Índice](#índice)

---

## Pruebas y calidad

La suite cuenta con **179 pruebas**: dominio, casos de uso, infraestructura (con un Funnel simulado), pantallas
Textual con las hojas de estilo reales, sistemas de init, seguridad. El código se verifica con `ruff`, `mypy` e
`import-linter` (reglas de las capas). La carpeta `tests/` se incluye en el archivo.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

La mayoría de las pruebas no necesitan ni Tailscale, ni HAProxy, ni root.

[↑ Índice](#índice)

---

## Estado del proyecto

### Puntos operativos

- Control completo de Tailscale: servicio, conexión, ajustes, publicación, red, registros.
- Puerta HAProxy antes de TLS, en producción desde el 2026-11-23, con reglas, listas, agrupaciones y modo ataque.
- Supervivencia: confinamiento, disyuntor, vigilancia automática.
- Escudo del puerto WireGuard, en producción desde el 2026-11-24.
- Informe y exportaciones TXT, HTML, JSON.
- Compatible con omega-connect y omega-fire.

### Limitaciones conocidas

- Los servicios con OpenRC y runit están cubiertos por las pruebas, pero todavía no se han validado en una máquina
  real.
- La puerta protege un Funnel publicado en HTTPS en un único puerto, con la ruta `/`.
- Las agrupaciones requieren un HAProxy compilado con Lua; sin Lua, la puerta funciona sin ellas.
- El escudo no puede colocarse en un núcleo actualizado sin reinicio (módulos ausentes): la pantalla lo indica.
- Un ataque que sature la propia línea de Internet queda fuera del alcance de una herramienta instalada en la
  máquina.
- El rendimiento de un sitio publicado mediante Funnel sigue limitado por los relés de Tailscale y por el router.

[↑ Índice](#índice)

---

## Desinstalación

Retire primero, desde omega-tail, lo que se ha colocado en el sistema, en este orden:

1. **Cortafuegos Funnel → Desactivar la protección** (Funnel se restablece como antes).
2. **Supervivencia → Desactivar la vigilancia**.
3. **Supervivencia → Escudo del puerto WireGuard → Retirar**.
4. **Supervivencia → Retirar el confinamiento**.

Después elimine la carpeta:

```bash
rm -rf ~/omega-tail
```

Elimine a mano las exportaciones colocadas en otro lugar, el alias `omega-tail` de `~/.bashrc` o `~/.zshrc` y, si
lo había activado, el archivo `/etc/sysctl.d/99-omega-tail-forwarding.conf`. El derecho de operador de Tailscale
se retira con `sudo tailscale set --operator=`.

[↑ Índice](#índice)

---

## Licencia

Omega-Tail se distribuye bajo licencia **MIT**. Consulte el archivo [`LICENSE`](../../../LICENSE) para el texto
completo.

La base AS / país utiliza IP Geolocation by [DB-IP](https://db-ip.com), bajo licencia
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Índice](#índice)

---

> **Omega-Tail — Controlar Tailscale, proteger Funnel.**
>
> Una interfaz TUI para Tailscale, y una puerta que rechaza los abusos antes de cualquier cifrado.
