<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem xmlns="http://www.battlescribe.net/schema/gameSystemSchema" name="Middlehammer Unification (Rules Prototype)" id="sys-middlehammer-2026" revision="1" battleScribeVersion="2.03" type="gameSystem">
  <comment>Rules prototype based on The Book of the Unification v1.7.2. Current catalogues remain original placeholder test data, not official codex units.</comment>
  <forceEntries>
    <forceEntry name="Standard Force Organization (5th Edition)" id="mh-test-force" hidden="false">
      <categoryLinks>
        <categoryLink name="HQ" hidden="false" id="mh-foc-0" targetId="ac8d-efba-1884-d3ad">
          <constraints>
            <constraint type="min" value="1" field="selections" scope="force" shared="true" id="mh-foc-0-min"/>
            <constraint type="max" value="2" field="selections" scope="force" shared="true" id="mh-foc-0-max"/>
          </constraints>
        </categoryLink>
        <categoryLink name="Troops" hidden="false" id="mh-foc-1" targetId="default-category">
          <constraints>
            <constraint type="min" value="2" field="selections" scope="force" shared="true" id="mh-foc-1-min"/>
            <constraint type="max" value="6" field="selections" scope="force" shared="true" id="mh-foc-1-max"/>
          </constraints>
        </categoryLink>
        <categoryLink name="Elites" hidden="false" id="mh-foc-2" targetId="978c-e18f-8aeb-f4c1">
          <constraints>
            <constraint type="min" value="0" field="selections" scope="force" shared="true" id="mh-foc-2-min"/>
            <constraint type="max" value="3" field="selections" scope="force" shared="true" id="mh-foc-2-max"/>
          </constraints>
        </categoryLink>
        <categoryLink name="Fast Attack" hidden="false" id="mh-foc-3" targetId="74fe-37c3-fbbf-849e">
          <constraints>
            <constraint type="min" value="0" field="selections" scope="force" shared="true" id="mh-foc-3-min"/>
            <constraint type="max" value="3" field="selections" scope="force" shared="true" id="mh-foc-3-max"/>
          </constraints>
        </categoryLink>
        <categoryLink name="Heavy Support" hidden="false" id="mh-foc-4" targetId="9260-7d57-be5c-bd52">
          <constraints>
            <constraint type="min" value="0" field="selections" scope="force" shared="true" id="mh-foc-4-min"/>
            <constraint type="max" value="3" field="selections" scope="force" shared="true" id="mh-foc-4-max"/>
          </constraints>
        </categoryLink>
      </categoryLinks>
    </forceEntry>
  </forceEntries>
  <categoryEntries>
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
