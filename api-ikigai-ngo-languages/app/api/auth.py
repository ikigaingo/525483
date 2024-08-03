import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Variables de configuración de Cognito
COGNITO_ISSUER = 'https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_evTJ0FgFG'
#https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_evTJ0FgFG'
USER_POOL_ID = 'ap-southeast-2_evTJ0FgFG'


def validate_token(token: str, issuer: str, user_pool_id: str):
    jwks_url = 'https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_evTJ0FgFG/.well-known/jwks.json'
    jwk_client = PyJWKClient(jwks_url)
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    try:
        decoded_token = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=user_pool_id,
            issuer=issuer
        )
        return decoded_token
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f'Invalid token: {e}')


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    return validate_token(token, COGNITO_ISSUER, USER_POOL_ID)
