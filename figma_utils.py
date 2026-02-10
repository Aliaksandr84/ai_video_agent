import requests

def list_top_frames(figma_token, file_key):
    """Get top-level frames in the Figma file."""
    headers = {'X-Figma-Token': figma_token}
    url = f'https://api.figma.com/v1/files/{file_key}'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    doc = resp.json()
    frames = []
    for page in doc['document']['children']:
        if page['type'] == 'CANVAS':  # each page
            for node in page['children']:
                if node['type'] == 'FRAME':
                    frames.append({
                        'id': node['id'],
                        'name': node['name'],
                        'page': page['name']
                    })
    return frames

def get_frame_image_url(figma_token, file_key, frame_id):
    """Fetch PNG image URL for the given frame/node in a Figma file."""
    headers = {'X-Figma-Token': figma_token}
    url = f'https://api.figma.com/v1/images/{file_key}?ids={frame_id}&format=png'
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()['images'][frame_id]