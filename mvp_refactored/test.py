from tabulate import tabulate
import mapper_utils
import os

IMAGE_DIR = 'images'
VALID_IMAGE_FILES = ['png', 'jpeg', 'jpg']
SEPERATOR = '********************************************************************'

# Attempts to identify and map calories for all images in the specified IMAGE_DIR
# Logs success and failure rates and metrics
# Image counts limited to 5 due to API restrictions
def run_test():
    print(SEPERATOR, '\nRunning tests...')
    results = [['EXPECTED LABEL', 'PREDICTED LABEL', 'CALORIE COUNT', 'CONFIDENCE SCORE', 'TEST STATUS', 'COMMENTS']]
    images = [f for f in os.listdir(IMAGE_DIR)]
    pass_count, failure_count = 0, 0
    for image in images:
        split = image.split('.')
        if (len(split) == 2) and (split[1] in VALID_IMAGE_FILES):
            expected_lbl = split[0]
            res = [expected_lbl]
            img_path = IMAGE_DIR+'/'+image
            label, calories, confidence = mapper_utils.identify_image(img_path)
            comment = 'Successful'
            if (label == expected_lbl):
                status = "Pass"
                pass_count += 1
            else:
                status = "Fail"
                failure_count += 1
                comment = 'Image identification failed' if calories else 'Calorie matching failed'
                
            res.extend([label, calories, confidence, status, comment])
            results.append(res)
    print('Generating report...')
    
    print(tabulate(results, headers='firstrow', tablefmt='fancy_grid'))

    total_tests = len(results)-1
    print('\n\n\nTest Stats:')
    print(f'Total images found in directory >>> {total_tests}')
    print(f'Success rate >>> {pass_count}/{total_tests} test cases ({round(pass_count*100/total_tests, 2)}%)')
    print(f'Failure rate >>> {failure_count}/{total_tests} test cases ({round(failure_count*100/total_tests, 2)}%)')

    print('Done!\n', SEPERATOR)

run_test()
