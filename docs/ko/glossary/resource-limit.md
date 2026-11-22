# Resource limit

Resource limit은 작업이 사용할 수 있는 메모리, 디스크 공간, CPU 시간, 동시 worker 수 등에 상한을 둔다. 작업이 어떤 파일이나 서비스에 접근할 수 있는지는 결정하지 않는다.

예를 들어 디스크 한도를 설정하면 agent의 빌드가 스토리지를 가득 채우는 것을 막을 수 있다. 하지만 실수로 노출된 디렉터리에서 빌드가 데이터를 읽는 것은 막지 못한다. 접근은 [policy](policy.md)로 별도로 제어한다.

[Resource limits](../practice/operations/resource-limits.md)를 참고한다.
