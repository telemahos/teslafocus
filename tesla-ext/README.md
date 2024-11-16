# tesla-ext
Tesla Used Invetory Extension
Extract Tesla data from the current page


document.querySelector('h1').textContent = chrome.i18n.getMessage('extensionName');
document.querySelector('p').textContent = chrome.i18n.getMessage('welcomeMessage');


<h1 data-i18n="extensionName"></h1>
<p data-i18n="welcomeMessage"></p>

<script>
  document.querySelectorAll('[data-i18n]').forEach(function(element) {
    const messageKey = element.getAttribute('data-i18n');
    element.textContent = chrome.i18n.getMessage(messageKey);
  });
</script>
########
Ja, alle diese Berechtigungen werden in deiner Extension genutzt:

"webRequest": Wird verwendet, um API-Anfragen an die Tesla-API zu überwachen und Metadaten der Anfragen zu speichern.
"storage": Wird verwendet, um Daten lokal im chrome.storage.local zu speichern und darauf zuzugreifen.
"tabs": Ermöglicht das Abrufen von Informationen über die aktuellen Tabs (z. B. aktiver Tab oder URL-Abgleich).
"activeTab": Gewährt temporären Zugriff auf den Inhalt des aktiven Tabs, was für die Kommunikation mit content.js notwendig ist.
"scripting": Ermöglicht das Einfügen und Ausführen von Skripten im aktuellen Tab, z. B. um extractIds() auszuführen.
###########
