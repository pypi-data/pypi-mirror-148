.. _admin:

.. raw:: html

    <br>

.. title:: admin

**NAME**

 **GENOCIDE** - Prosecutor. Reconsider. OTP-CR-117/19.

**SYNOPSIS**

 ``gcidctl <cmd> [key=value] [key==value]``

**DESCRIPTION**

 **GENOCIDE** is a python3 program that holds evidence that the king of the
 netherlands is doing a genocide, a written response where the king of
 the netherlands confirmed taking note of “what i have written”, namely
 proof that medicine he uses in treatement laws like zyprexa, haldol,
 abilify and clozapine are poison that makes impotent, is both physical
 (contracted muscles) and mental (let people hallucinate) torture and kills
 members of the victim groups,  source is :ref:`here <source>`.

 **GENOCIDE** contains correspondence with the International Criminal Court, 
 asking for arrest of the king of the netherlands, for the genocide he is
 committing with his new treatement laws. Current status is an outside the
 jurisdiction judgement of the prosecutor which requires a reconsider to have
 the king actually arrested.

 **GENOCIDE** provides a IRC bot that can run as a background daemon for 24/7
 day presence in a IRC channel, be used to display RSS feeds, act as a UDP
 to IRC gateway and program your own commands for.

**INSTALL**

 ``pip3 install gcid``

**CONFIGURATION**

 | ``cp /usr/local/share/gcid/gcid.service /etc/systemd/system``
 | ``systemctl enable gcid --now``

 *irc*

 | ``gcidctl cfg server=<server> channel=<channel>``
 | ``gcidctl cfg nick=<nick>``

 default channel/server is #genocide on localhost

 *sasl*

 | ``gcidctl pwd <nickservnick> <nickservpass>``
 | ``gcidctl cfg password=<outputfrompwd>``

 *users*

 | ``gcidctl cfg users=True``
 | ``gcidctl met <userhost>``

**COPYRIGHT**

 **GCID** is placed in the Public Domain. No Copyright, No License.

**AUTHOR**

 Bart Thate - bthate67@gmail.com
