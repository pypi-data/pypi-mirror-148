from aws_cdk.core import App

from b_cfn_custom_api_key_authorizer_test.integration.infrastructure.main_stack import MainStack

app = App()
MainStack(app)
app.synth()
