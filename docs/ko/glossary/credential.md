# Credential

Credential은 서비스가 누가 요청하는지 또는 요청자에게 어떤 접근 권한이 있는지 확인하는 데 쓰는 정보다. 예를 들어 API token은 프로그램이 접근 권한을 얻기 위해 서비스에 보낼 수 있는 값이다. Sandbox의 코드가 재사용 가능한 credential을 받으면, 의도한 한 가지 작업 외에도 그 credential을 사용할 수 있다.

## 예시

Sandbox에 이슈 제목이 필요하다. Sandbox 외부에서 실행되는 [tool](tool.md)이 해당 이슈가 승인된 프로젝트에 속하는지 확인한다. Tool은 이슈 추적기에 읽기 전용 token을 보내고 sandbox에는 제목을 반환한다. Token은 tool과 이슈 추적기가 처리하며, sandbox의 코드는 제목만 받는다.

## 누가 사용할 수 있는가

유효한 [bearer token](https://www.rfc-editor.org/rfc/rfc6750.html#section-1.2)을 얻은 사람은 누구든 서비스가 해당 token을 받아들이는 곳에서 사용할 수 있다. Sandbox의 코드가 파일이나 프로그램 설정에서 token을 읽을 수 있다면 그 token을 직접 사용할 수 있다. Token의 복사본이 로그나 프로그램의 메모리를 저장하는 [snapshot](snapshot.md)에 남을 수도 있다.

[least privilege](least-privilege.md)를 적용한다. 작업에 필요한 동작과 리소스에만 접근 권한을 부여하고 유효 기간이 짧은 credential을 우선 사용한다. 코드에 credential이 아니라 결과만 필요하다면 host tool이나 [credential injection](credential-injection.md)으로 credential이 프로그램에 전달되지 않도록 할 수 있다.

[용어집으로 돌아가기](../glossary.md)
