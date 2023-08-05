from ubuntu:20.04
ENV CARGO_HOME=/opt/rust RUSTUP_HOME=/opt/rust
ENV PATH=/opt/rust/bin:${PATH}
run apt-get update && apt-get install --no-install-recommends -y curl ca-certificates python3-pip build-essential
run curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile default
run pip3 install maturin
copy .pypirc /root/
copy . . 
run maturin publish