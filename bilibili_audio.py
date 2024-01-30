import ffmpeg, os, sys, multiprocessing, json

def get_files(in_root, out_root):
    files = list()
    l1 = os.listdir(in_root)
    for l11 in l1:
        l2 = os.listdir(os.path.join(in_root, l11))
        for l22 in l2:
            jf = open(os.path.join(in_root, l11, l22, 'entry.json'), 'r', encoding='utf-8')
            jd = json.load(jf)
            jf.close()
            title_1 = jd['title']
            if 'part' in jd['page_data']:
                title_2 = jd['page_data']['part']
            else:
                title_2 = title_1
            title_1 = title_1.replace(' ', '_')
            title_1 = title_1.replace("\\", "_")
            title_1 = title_1.replace("/", "_")
            title_1 = title_1.replace("|", "_")
            title_2 = title_2.replace(' ', '_')
            title_2 = title_2.replace("\\", "_")
            title_2 = title_2.replace("/", "_")
            title_2 = title_2.replace("|", "_")

            if title_1 != title_2:
                files.append(((in_root, l11, l22), (out_root, title_1, title_2)))
            else:
                files.append(((in_root, l11, l22), (out_root, title_1)))
    return files


def process(in_path, out_path, fmt='mp3'):
    in_path += ('16', 'audio.m4s')
    stream = ffmpeg.input(os.path.join(*in_path))
    audio = stream.audio
    out_path = out_path[:-1] + (out_path[-1]+"."+fmt,)
    os.makedirs(os.path.join(*out_path[:-1]), exist_ok=True)
    if fmt == 'mp3':
        out = ffmpeg.output(audio, os.path.join(*out_path), acodec='libmp3lame')
    else:
        out = ffmpeg.output(audio, os.path.join(*out_path))
    out.run()
    return True


if __name__ == '__main__':
    in_root = './data/gtasa'
    out_root = './data/gtasa_converted'
    files = get_files(in_root, out_root)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    rets = list()
    for file in files:
        rets.append(pool.apply_async(process, file))

    pool.close()
    pool.join()
    for ret in rets:
        ret.get()
