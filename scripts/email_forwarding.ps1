$s = New-PSsession -ConfigurationName microsoft.exchange -ConnectionUri http://exchange.pocketnurse.com/powershell

Import-PSSession $s

Set-Mailbox -Identity "${FIRST} ${LAST}" -ForwardingAddress "${USERNAME}@pocketnurse.com" -DeliverToMailboxAndForward $true