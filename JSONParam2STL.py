#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

import os
import json

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        design = app.activeProduct
        if not design:
            ui.messageBox('アクティブなデザインがありません。')
            return
            
        fileDlg = ui.createFileDialog()
        fileDlg.title = 'パラメーター設定JSONファイルを選択'
        fileDlg.filter = 'JSON files (*.json);;All files (*.*)'
        if fileDlg.showOpen() != adsk.core.DialogResults.DialogOK:
            return
        jsonPath = fileDlg.filename
        
        with open(jsonPath, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        parameterSets = config.get('parameter_sets', [])
        stl_settings = config.get('stl_settings', {})
        
        # STL設定のデフォルト値を設定
        default_stl_settings = {
            'refinement': 'medium',  # low, medium, high
            'surface_deviation': 0,  # カスタム値（0の場合は使用しない）
            'normal_deviation': 0,    # カスタム値（0の場合は使用しない）
            'max_edge_length': 0,     # カスタム値（0の場合は使用しない）
            'aspect_ratio': 0,        # カスタム値（0の場合は使用しない）
            'output_folder': '',      # 空の場合はダイアログで選択
            'unit_type': 'cm'        # mm, cm, m, inch
        }
        
        stl_settings = {**default_stl_settings, **stl_settings}
        
        if not stl_settings['output_folder']:
            folderDlg = ui.createFolderDialog()
            folderDlg.title = 'エクスポート先フォルダを選択'
            if folderDlg.showDialog() != adsk.core.DialogResults.DialogOK:
                return
            exportFolder = folderDlg.folder
        else:
            exportFolder = os.path.expanduser(stl_settings['output_folder'])
            if not os.path.exists(exportFolder):
                os.makedirs(exportFolder)
        
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = 'キャンセル'
        progressDialog.show('STLエクスポート', '処理中... %p%', 0, len(parameterSets), 1)
        
        params = design.allParameters
        
        original_values = {}
        for paramSet in parameterSets:
            for paramName in paramSet.get('parameters', {}).keys():
                param = params.itemByName(paramName)
                if param and paramName not in original_values:
                    original_values[paramName] = param.expression

        try:
            for i, paramSet in enumerate(parameterSets):
                if progressDialog.wasCancelled:
                    break
                    
                progressDialog.message = f'パラメーター設定 "{paramSet.get("name", f"set_{i}")}" を処理中...'
                
                parameters = paramSet.get('parameters', {})
                for paramName, value in parameters.items():
                    try:
                        param = params.itemByName(paramName)
                        if param:
                            if isinstance(value, str):
                                param.expression = value
                            else:
                                param.value = value
                    except:
                        ui.messageBox(f'パラメーター "{paramName}" の設定に失敗しました。')
                
                adsk.doEvents()
                app.activeViewport.refresh()
                
                rootComp = design.rootComponent
                allBodies = []
                
                for occurrence in rootComp.allOccurrences:
                    if occurrence.isVisible:
                        for body in occurrence.bRepBodies:
                            if body.isVisible:
                                allBodies.append(body)
                
                for body in rootComp.bRepBodies:
                    if body.isVisible:
                        allBodies.append(body)
                
                setName = paramSet.get('name', f'set_{i}')
                for body in allBodies:
                    exportMgr = design.exportManager
                    stlOptions = exportMgr.createSTLExportOptions(body)
                    
                    # メッシュ精度の設定
                    refinement_map = {
                        'low': adsk.fusion.MeshRefinementSettings.MeshRefinementLow,
                        'medium': adsk.fusion.MeshRefinementSettings.MeshRefinementMedium,
                        'high': adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
                    }
                    stlOptions.meshRefinement = refinement_map.get(
                        stl_settings['refinement'].lower(),
                        adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
                    )
                    
                    # 単位の設定
                    unit_type = stl_settings['unit_type'].lower()
                    if unit_type == 'mm':
                        stlOptions.isMillimeterUnits = True
                        stlOptions.isCentimeterUnits = False
                        stlOptions.isMeterUnits = False
                        stlOptions.isInchUnits = False
                    elif unit_type == 'cm':
                        stlOptions.isMillimeterUnits = False
                        stlOptions.isCentimeterUnits = True
                        stlOptions.isMeterUnits = False
                        stlOptions.isInchUnits = False
                    elif unit_type == 'm':
                        stlOptions.isMillimeterUnits = False
                        stlOptions.isCentimeterUnits = False
                        stlOptions.isMeterUnits = True
                        stlOptions.isInchUnits = False
                    elif unit_type == 'inch':
                        stlOptions.isMillimeterUnits = False
                        stlOptions.isCentimeterUnits = False
                        stlOptions.isMeterUnits = False
                        stlOptions.isInchUnits = True
                    
                    # カスタムメッシュ設定
                    if stl_settings['surface_deviation'] > 0:
                        stlOptions.surfaceDeviation = stl_settings['surface_deviation']
                    if stl_settings['normal_deviation'] > 0:
                        stlOptions.normalDeviation = stl_settings['normal_deviation']
                    if stl_settings['max_edge_length'] > 0:
                        stlOptions.maxEdgeLength = stl_settings['max_edge_length']
                    if stl_settings['aspect_ratio'] > 0:
                        stlOptions.aspectRatio = stl_settings['aspect_ratio']
                    
                    filename = f"{body.name}_{setName}.stl"
                    filename = filename.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
                    filepath = os.path.join(exportFolder, filename)
                    
                    stlOptions.filename = filepath
                    exportMgr.execute(stlOptions)
                
                progressDialog.progressValue = i + 1
                
        finally:
            progressDialog.message = 'パラメーターを元に戻しています...'
            
            for paramName, originalValue in original_values.items():
                try:
                    param = params.itemByName(paramName)
                    if param:
                        param.expression = originalValue
                except:
                    ui.messageBox(f'パラメーター "{paramName}" の復元に失敗しました。')
            
            adsk.doEvents()
            app.activeViewport.refresh()
            
        progressDialog.hide()
        ui.messageBox('エクスポートが完了しました。\nパラメーターは元の値に戻されました。')
        
    except:
        if ui:
            ui.messageBox('エラーが発生しました:\n{}'.format(traceback.format_exc()))