<template>
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6"> Datenschutz Richtlinien </h1>



      
      <div class="space-y-6">
        <section>
          <h2 class="text-2xl font-semibold mb-4">1. Geltungsbereich </h2>
          <p class="mb-4">
            Diese Nutzungsbedingungen regeln die Nutzung der WebApp der Universität Graz/Institut für Biologie im Rahmen des Forschungsprojekts zur Erforschung von Flechten und kryptogamen Gemeinschaften. Die WebApp „CC-Explorer“ ist ein Projekt des Instituts für Biologie und wird zur Erkennung und langfristigen Beobachtung von „kryptogamen Gemeinschaften“ verwendet. Diese Gemeinschaften setzen sich aus Moosen, Flechten, Pilzen und Cyanobakterien zusammen. Sie sind für viele Klimaprozesse relevant, stabilisieren den Boden und sind zb. Marker für Luftqualität. Die Webapp bietet einerseits Informationen über diese Organismen und dient Nutzern, die sich aktiv an der Forschung beteiligen wollen („Citizen Scientist“) als Portal um Beobachtungen in Form von Smartphone-Bildern hochzuladen. Für richtige Aufzeichnung sind Richtlinien bereitgestellt. Nach dem Upload werden die Bilder automatisiert verarbeitet, bestimmte Organsimen werden mit Methoden des maschinellen Lernens erkannt und die Ergebnisse werden öffentlich zur Verfügung gestellt. Die Datenverarbeitung umfasst die hochgeladenen Bilder, Standortinformationen (für weitere Analysen und Darstellungen) sowie die genaue Uhrzeit des Hochladens (zum Zweck der Langzeitbeobachtung).
            CC-Explorer
            https://cc-explorer.com (noch nicht online)
          </p>
        </section>
  
        <section>
          <h2 class="text-2xl font-semibold mb-4"> 2. Nutzungsberechtigung </h2>
          <p class="mb-4">
            •	Die Nutzung der WebApp ist ab einem Alter von 14 Jahren zulässig
            •	Die Nutzung ist kostenfrei
            •	Der Zugriff auf den Informationsbereich erfolgt ohne Anmeldung
            •	Die Teilnahme an der Forschung erfordert eine Registrierung
          </p>
        </section>
  
        <section>
          <h2 class="text-2xl font-semibold mb-4">3. Data Storage</h2>
          <p class="mb-4">
            [Describe how and where you store the data]
          </p>
        </section>
  
        <section>
          <h2 class="text-2xl font-semibold mb-4">4. User Rights</h2>
          <p class="mb-4">
            [Explain user rights regarding their data]
          </p>
          <ul class="list-disc ml-6">
            <li>Right to access their data</li>
            <li>Right to correct their data</li>
            <li>Right to delete their data</li>
            <li>Right to withdraw consent</li>
          </ul>
        </section>
  
        <section>
          <h2 class="text-2xl font-semibold mb-4">5. Contact Information</h2>
          <p class="mb-4">
            For any questions regarding this privacy policy, please contact:
          </p>
          <div class="ml-4">
            <p>[Your Organization Name]</p>
            <p>[Address]</p>
            <p>Email: [contact@email.com]</p>
            <p>Phone: [phone number]</p>
          </div>
        </section>
  
        <section>
          <h2 class="text-2xl font-semibold mb-4">6. Updates to This Policy</h2>
          <p class="mb-4">
            [Explain how and when you update the policy]
          </p>
          <p class="italic">
            Last updated: [Date]
          </p>
        </section>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PrivacyView',
    mounted() {
      document.title = 'Privacy Policy - [Your App Name]'
    }
  }
  </script>