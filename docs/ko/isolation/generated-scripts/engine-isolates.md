# Engine isolate 사용 방식 {#engine-isolates}

[engine isolate](../../glossary/engine-isolate.md)는 [V8](https://github.com/v8/v8/blob/13.8.258/include/v8-isolate.h#L277-L285) 같은 언어 엔진 안에서 스크립트의 객체와 실행 상태를 다른 스크립트와 분리합니다. 엔진을 내장한 플랫폼이 코드에서 사용할 수 있는 API를 정합니다.

## 누가 요청을 처리하나요? {#who-handles-the-request}

스크립트가 [`LAMP-17`](../../practice/design/from-issue-to-patch.md)의 제목을 요청하면 엔진은 스크립트를 실행하고, 플랫폼은 이름이 지정된 연결을 통해 이슈 서비스로 요청을 전달합니다. 이슈 서비스는 해당 이슈에 대한 [authorization](../../glossary/authorization.md)을 확인한 뒤 제목을 반환합니다.

[Cloudflare Dynamic Workers](https://blog.cloudflare.com/dynamic-workers/)는 JavaScript에 이런 실행 환경을 제공합니다. Cloudflare 문서의 예에서 호출자는 `globalOutbound: null`로 설정해 일반적인 외부 요청을 막으면서도 특정 **binding**을 제공할 수 있습니다. Binding은 이름을 붙여 둔 다른 서비스 연결입니다.

## 무엇을 계속 공유하나요? {#what-stays-shared}

엔진은 isolate마다 스크립트 상태를 분리하지만, 여러 isolate가 하나의 운영체제 [process](../../glossary/process.md)를 공유할 수 있습니다. 플랫폼은 여러 isolate를 같은 서비스에 연결할 수도 있습니다. Isolate는 별도의 process나 [VM](../../glossary/virtual-machine.md)이 아닙니다.

## 언제 사용하나요? {#when-to-use-it}

스크립트에 언어 엔진의 기능과 일부 플랫폼 API가 필요하지만 셸이나 native 패키지는 필요 없을 때 이 경계를 선택합니다.

## 이 경계가 보호하지 않는 범위 {#what-the-boundary-does-not-cover}

임의의 URL에서 데이터를 가져올 수 있는 binding은 스크립트가 직접 네트워크 요청을 보낼 수 없더라도 넓은 접근 권한을 부여합니다. Worker의 binding과 기본 네트워크 접근 권한을 함께 검토하세요. 어떤 스크립트가 process를 공유하는지, 플랫폼이 엔진 주변에 어떤 추가 제어를 적용하는지도 확인하세요.
