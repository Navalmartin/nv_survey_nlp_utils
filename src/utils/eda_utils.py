import os
import time
from typing import List
from pathlib import Path

import fitz


def count_document_number_of_pages(document_path: Path) -> tuple:
    with fitz.open(document_path) as pdf:
        # Get the filename
        fname = document_path.name
        num_pages = len(pdf)
        return fname, num_pages


def count_document_number_of_images(document_path: Path) -> int:
    with fitz.open(document_path) as pdf:
        num_pages_with_images = 0
        for page_num, page in enumerate(pdf):
            image_list = page.get_images()
            if len(image_list) >= 1:
                num_pages_with_images += 1
        return  num_pages_with_images


def count_images_per_page(pdf_dir):
    results = []
    for pdf_path in Path(pdf_dir).glob("*.pdf"):
        with fitz.open(pdf_path) as pdf:
            num_pages_with_images = 0
            for page_num, page in enumerate(pdf):
                image_list = page.get_images()
                if len(image_list) >= 1:
                    num_pages_with_images += 1
            results.append(
                {
                    "filename": pdf_path.name,
                    "num_pages_with_images": num_pages_with_images,
                }
            )
    return results


def text_from_pdf_to_txt(pdf_path: Path, output_dir: Path,
                         encoding: str = "utf8"):

    with fitz.open(pdf_path) as pdf:
        # Get the filename without the ".pdf" suffix
        fname = os.path.splitext(pdf_path.name)[0]
        out_path = output_dir / (fname + ".txt")
        with open(out_path, "wb") as out:  # open text output
            for page in pdf:  # iterate the document pages
                text = page.get_text().encode(encoding)
                out.write(text)  # write text of page
                out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
            out.close()


def get_section_text(pdf_path: Path,
                     section: str,
                     encoding: str = "utf8") -> List[tuple]:

    pages_found = []
    with fitz.open(pdf_path) as pdf:
        for page in pdf:

            found = page.search_for(section)

            if len(found) != 0:
                pages_found.append((found, page.get_text()))
    return pages_found


def download_survey_pdf(drive, survey, surveys_local_dir, surveys_output_dir):
    id = survey["id"]
    name = survey["name"]
    # Get the base filename without extension
    pdf_basename = os.path.splitext(name)[0]
    txt_file = pdf_basename + ".txt"
    if txt_file in os.listdir(surveys_output_dir):
        print(f"{name} has a corresponding {txt_file} in the output folder.")
    else:
        # Download pdf file codition_surveys folder:
        drive.download_item(
            item_id=f"{id}", file_path=str(surveys_local_dir) + "/" + f"{name}"
        )


def get_number_of_files_in_dir(directory: Path):
    
    
    num_files = len(
        [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    )
    return num_files


def count_files_for_key(files: List[Path], key: str) -> dict:

    result = {key: 0}
    for filename in files:
        components = str(filename).split("/")

        if key in components:
            result[key] += 1
    return result


def get_files_in_dir(base_dir: Path, file_formats: List[str],
                    files_out: List[Path]) -> List[Path]:
    
    # load the corrosion images
    files = os.listdir(base_dir)
    for filename in files:
        if os.path.isfile(base_dir / filename):
            filename_, file_extension = os.path.splitext(filename)
            
            if file_extension in file_formats:
                files_out.append(base_dir / filename)
            else:
                continue
        elif os.path.isdir(base_dir / filename):
            get_files_in_dir(base_dir=base_dir / filename,
                             file_formats=file_formats,
                             files_out=files_out)


def _recoverpix(doc, item):
    xref = item[0]  # xref of PDF image
    smask = item[1]  # xref of its /SMask

    # special case: /SMask or /Mask exists
    if smask > 0:
        pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
        if pix0.alpha:  # catch irregular situation
            pix0 = fitz.Pixmap(pix0, 0)  # remove alpha channel
        mask = fitz.Pixmap(doc.extract_image(smask)["image"])

        try:
            pix = fitz.Pixmap(pix0, mask)
        except:  # fallback to original base image in case of problems
            pix = fitz.Pixmap(doc.extract_image(xref)["image"])

        if pix0.n > 3:
            ext = "pam"
        else:
            ext = "png"

        return {  # create dictionary expected by caller
            "ext": ext,
            "colorspace": pix.colorspace.n,
            "image": pix.tobytes(ext),
        }

    # special case: /ColorSpace definition exists
    # to be sure, we convert these cases to RGB PNG images
    if "/ColorSpace" in doc.xref_object(xref, compressed=True):
        pix = fitz.Pixmap(doc, xref)
        pix = fitz.Pixmap(fitz.csRGB, pix)
        return {  # create dictionary expected by caller
            "ext": "png",
            "colorspace": 3,
            "image": pix.tobytes("png"),
        }
    return doc.extract_image(xref)


def extract_images(pdf_path, dimlimit, relsize, abssize, imgdir):
    # The following values should go into a config file
    # dimlimit = 0  # 100  # each image side must be greater than this
    # relsize = 0  # 0.05  # image : image size ratio must be larger than this (5%)
    # abssize = 0  # 2048  # absolute image size limit 2 KB: ignore if smaller
    # imgdir = "output"  # found images are stored in this subfolder

    with fitz.open(pdf_path) as doc:
        t0 = time.time()

        page_count = doc.page_count  # number of pages

        xreflist = []
        imglist = []
        for pno in range(page_count):
            il = doc.get_page_images(pno)
            imglist.extend([x[0] for x in il])
            for img in il:
                xref = img[0]
                if xref in xreflist:
                    continue
                width = img[2]
                height = img[3]
                if min(width, height) <= dimlimit:
                    continue
                image = _recoverpix(doc, img)
                n = image["colorspace"]
                imgdata = image["image"]

                if len(imgdata) <= abssize:
                    continue
                if len(imgdata) / (width * height * n) <= relsize:
                    continue

                imgfile = os.path.join(imgdir, "img%05i.%s" % (xref, image["ext"]))
                fout = open(imgfile, "wb")
                fout.write(imgdata)
                fout.close()
                xreflist.append(xref)

        t1 = time.time()
        imglist = list(set(imglist))
        print(len(set(imglist)), "images in total")
        print(len(xreflist), "images extracted")
        print("total time %g sec" % (t1 - t0))
