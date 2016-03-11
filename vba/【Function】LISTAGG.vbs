' 2015-03-19
' 参照LOOKUP和VLOOKUP参数设置；
' 参考lookup参数设置
' lookup_value 第一个矢量中搜索到的值
' lookup_vector 是一个仅包含一列的区域
' result_vector 是一个仅包含一列的区域
' Optional ch As String = ","：合并后的分割符，可自定义，默认为英文逗号（”,”）
' 【后续处理】可选参数的容错处理
Function LISTAGG(lookup_value As String, lookup_vector As Range, Optional result_vector As Range, Optional ch As String = ", ", Optional removal As Boolean = True)
    If result_vector Is Nothing Then
        result_vector = lookup_vector
    End If

    ' 定义查找列字母索引
    Dim lookupColLetter As String
    lookupColLetter = ColLetter(lookup_vector.Column)

    ' 定义查找列开始、结束行索引位置
    Dim startRowIndex As Long, endRowIndex As Long
    startRowIndex = lookup_vector.Row
    endRowIndex = lookup_vector.Rows.Count

    ' 定义开始、结束单元格式位置
    Dim startCellAddress As String, endCellAddress As String

    endCellAddress = lookupColLetter + Str(endRowIndex)
    endCellAddress = Replace(endCellAddress, " ", "")

    ' 定义返回结果集合
    Dim resultCollection As Collection
    Set resultCollection = New Collection

    ' 定义查找到的单元格内容
    Dim resultCellValue As String

    Dim lastAdrress As String
    lastAdrress = ""
    Do
        cCount = cCount + 1
        startCellAddress = lookupColLetter + Str(startRowIndex)
        startCellAddress = Replace(startCellAddress, " ", "")

        Set newLookupRange = Range(startCellAddress + ":" + endCellAddress)
        ' Set matchcell = newLookupRange.Find(what:=lookup_value)
        Set matchcell = newLookupRange.Find(what:=lookup_value, LookAt:=xlWhole)

        If matchcell Is Nothing Or lastAdrress = matchcell.Address Then
            GoTo exitLoop
        End If

        lastAdrress = matchcell.Address
        resultCellValue = Cells(matchcell.Row, result_vector.Column)

        If removal Then
            ' 去重
            If Contains(resultCollection, resultCellValue) = False Then
                resultCollection.Add resultCellValue
            End If
        End If

        startRowIndex = matchcell.Row
    Loop While 1 = 1

exitLoop:
    Dim i As Long ' 遍历索引
    For i = 1 To resultCollection.Count
        If LISTAGG <> "" Then
            LISTAGG = LISTAGG + ch
        End If

        LISTAGG = LISTAGG + resultCollection.Item(i)
    Next i

End Function

Private Function Contains(coll As Collection, v As String) As Boolean
    Dim i As Long

    Contains = False
    For i = 1 To coll.Count
        If v = coll.Item(i) Then
            Contains = True
            GoTo exitfor
        End If
    Next i
exitfor:

End Function

' 获取列字母
Function ColLetter(ColNumber As Integer) As String
    On Error GoTo Errorhandler
    ColLetter = Left(Cells(1, ColNumber).Address(0, 0), 1 - (ColNumber > 26))
    Exit Function

Errorhandler:
    MsgBox "Error encountered, please re‐enter "
End Function