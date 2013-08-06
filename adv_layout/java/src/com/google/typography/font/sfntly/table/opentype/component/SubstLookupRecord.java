package com.google.typography.font.sfntly.table.opentype.component;

import com.google.typography.font.sfntly.data.ReadableFontData;
import com.google.typography.font.sfntly.data.WritableFontData;

public final class SubstLookupRecord implements Record {
  public static final int RECORD_SIZE = 4;
  public static final int SEQUENCE_INDEX_OFFSET = 0;
  public static final int LOOKUP_LIST_INDEX_OFFSET = 2;
  public final int sequenceIndex;
  public final int lookupListIndex;

  public SubstLookupRecord(ReadableFontData data, int base) {
    this.sequenceIndex = data.readUShort(base + SEQUENCE_INDEX_OFFSET);
    this.lookupListIndex = data.readUShort(base + LOOKUP_LIST_INDEX_OFFSET);
  }

  public SubstLookupRecord(int sequenceIndex, int lookupListIndex) {
    this.sequenceIndex = sequenceIndex;
    this.lookupListIndex = lookupListIndex;
  }

  @Override
  public int writeTo(WritableFontData newData, int base) {
    newData.writeUShort(base + SEQUENCE_INDEX_OFFSET, sequenceIndex);
    newData.writeUShort(base + LOOKUP_LIST_INDEX_OFFSET, lookupListIndex);
    return RECORD_SIZE;
  }
}