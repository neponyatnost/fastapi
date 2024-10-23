from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List

router = APIRouter(
    prefix='/product',
    tags=['products']
)

products = [
    'apple',
    'banana',
    'cherry',
    'date',
    'elderberry',
    'fig',
    'grape',
    'honeydew',
]


@router.post('/new')
async def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get('/all')
async def get_all_products():
    data = ' '.join(products)
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key='test_cookie', value='test_cookie_value')
    return response


@router.get('/with-header')
async def get_products_with_header(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None)
):
    response.headers['my_custom_header_from_response'] = ', '.join(custom_header)
    return {
        'data': products,
        'custom_header': custom_header,
        'custom_cookie': test_cookie
    }


@router.get('/{id}', responses={
    200: {
        'content': {
            'text/html': {
                'example': '<div>Product</div>'
            }
        },
        'description': 'Returns the HTML for a product'
    },
    404: {
        'content': {
            'text/plain': {
                'example': 'Product not found.'
            }
        },
        'description': 'Plain text error message'
    }
})
async def get_product_by_id(id: int):
    if id > len(products):
        out = 'Product not available'
        return PlainTextResponse(content=out, media_type='text/plain')
    else:
        product = products[id]
        out = f"""
            <head>
                <title>{product}</title>
                <style>
                    .product {{
                        background-color: lightblue;
                        text-align: center;
                        border: 1px solid black;
                        width: 500px;
                        height: 100px;
                    }}
                </style>
            </head>
            <div class='product'>
                <p>This is a product:</p>
                <h1>{product}</h1>
            </div>
        """
        return HTMLResponse(content=out, media_type='text/html')
