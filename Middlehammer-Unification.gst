<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem xmlns="http://www.battlescribe.net/schema/gameSystemSchema" name="Middlehammer Unification — Import Smoke Test" id="sys-middlehammer-2026" revision="1" battleScribeVersion="2.03" type="gameSystem">
  <comment>Original smoke-test data only. These sample units are placeholders, not official codex data or Unification Patch rules.</comment>
  <forceEntries>\n    <forceEntry name="Test Detachment" id="mh-test-force" hidden="false">\n      <categoryLinks>\n        <categoryLink name="HQ" hidden="false" id="mh-force-hq" targetId="ac8d-efba-1884-d3ad"/>\n        <categoryLink name="Troops" hidden="false" id="mh-force-troops" targetId="default-category"/>\n      </categoryLinks>\n    </forceEntry>\n  </forceEntries>\n  <categoryEntries>
    <categoryEntry name="Troops" id="default-category" hidden="false"/>
    <categoryEntry name="HQ" id="ac8d-efba-1884-d3ad" hidden="false"/>
    <categoryEntry name="Elites" id="978c-e18f-8aeb-f4c1" hidden="false"/>
    <categoryEntry name="Fast Attack" id="74fe-37c3-fbbf-849e" hidden="false"/>
    <categoryEntry name="Heavy Support" id="9260-7d57-be5c-bd52" hidden="false"/>
    <categoryEntry name="Dedicated Transport" id="168b-a772-94f7-83f5" hidden="false"/>
  </categoryEntries>
  <costTypes>
    <costType name="Points" id="6f18-a8fc-2c5b-9517" defaultCostLimit="-1"/>
  </costTypes>
  <profileTypes>
    <profileType name="Abilities" id="ccb3-7790-3139-7975" hidden="false" kind="ability">
      <characteristicTypes><characteristicType name="Description" id="mh-ability-description"/></characteristicTypes>
    </profileType>
    <profileType name="Unit" id="0967-823d-dd82-4e47" hidden="false" kind="model">
      <characteristicTypes>
        <characteristicType name="WS" id="mh-unit-ws"/>
        <characteristicType name="BS" id="mh-unit-bs"/>
        <characteristicType name="S" id="mh-unit-s"/>
        <characteristicType name="T" id="mh-unit-t"/>
        <characteristicType name="W" id="mh-unit-w"/>
        <characteristicType name="I" id="mh-unit-i"/>
        <characteristicType name="A" id="mh-unit-a"/>
        <characteristicType name="Ld" id="mh-unit-ld"/>
        <characteristicType name="Sv" id="mh-unit-sv"/>
      </characteristicTypes>
    </profileType>
  </profileTypes>
</gameSystem>
